from flask import Flask, request, jsonify

import os
import json
import openai
from bobby import Bobby
from speak import Speak
from listen import Listen
from utils import SkillHelper, SYSTEM_MESSAGE
import pvporcupine
from pvrecorder import PvRecorder
from rich import print

CINFO = "[white][[/white][cyan]?[/cyan][white]][/white] [gray]-[/gray] [bright_yellow]"
CPROG = "[white][[/white][yellow]-[/yellow][white]][/white] [gray]-[/gray] [bright_yellow]"
CFERR = "[white][[/white][red]✗[/red][white]][/white] [gray]-[/gray] [bright_red]"
CSUCC = "[white][[/white][bright_green]✓[/bright_green][white]][/white] [gray]-[/gray] [bright_yellow]"

# ---------------------------------- CONFIG ---------------------------------- #

# the model to use - it should be one trained on function calling
MODEL = "gpt-3.5-turbo-0613"

# OpenAI API key - if left None, API_KEY will be the env variable OPENAI_API_KEY
API_KEY = None 

# list of skill names (string) to allow the virtual assistant to use, these
# skills must be placed in the skills.py file and subclass utils.Skill
SKILLS = [
    'EndConversation', # required by default to end the conversation
    'TurnLightsOff',
    'TurnLightsOn',
    'PlayMusic',
    'StopMusic',
]

# ---------------------------------- CONFIG ---------------------------------- #


if API_KEY is None:
    API_KEY = os.getenv("OPENAI_API_KEY")
    if API_KEY is None:
        raise Exception("Missing OPENAI_API_KEY environment variable and none provided in config")
openai.api_key = API_KEY

PORCUPINE_API_KEY = os.getenv("PORCUPINE_API_KEY")
if PORCUPINE_API_KEY is None:
    raise Exception("Missing PORCUPINE_API_KEY environment variable")

ppn = pvporcupine.create(
    access_key=PORCUPINE_API_KEY,
    keyword_paths=['heybobby.ppn']
)

recorder = PvRecorder(device_index=-1, frame_length=512)

listen = Listen(API_KEY)
    
skill_helper = SkillHelper(SKILLS)
bobby = Bobby(SYSTEM_MESSAGE, skill_helper.get_skills(), MODEL)
speak = Speak()

#--



app = Flask(__name__)

def process(text):
    message = {"role": "user", "content": text}
    while True:
        print(CINFO + "Getting response from OpenAI...")
        completion = bobby.get_response(message)
        if completion['finish_reason'] == 'function_call':
            print(CSUCC + "Got response from OpenAI")
            print(CINFO + "Processing response...")
            called_function_name = completion['message']["function_call"]["name"]
            called_function_args = completion['message']["function_call"]["arguments"]
            print(CINFO + "called_function_name: " + called_function_name)
            print(CINFO + "called_function_args: " + called_function_args)
            message = completion['message']
            print(CINFO + "[green]response: \"" + str(message))
            params = json.loads(called_function_args)
            if called_function_name == "EndConversation":
                print(CSUCC + "Conversation is over.")
                print(CINFO + "Synthesizing response audio...")
                audio = speak.save(params['message'])
                print(CSUCC + "Audio synthesized.")
                print(CINFO + audio)
                return audio
            #print("Function call: " + called_function_name + ", Args: " + called_function_args)
            skill_info = skill_helper.do_skill(called_function_name, params=params)
            message = {"role": "function", "name": called_function_name, "content": skill_info}
            #print("Function info: " + str(skill_info))
        elif completion['finish_reason'] == 'stop':
            print(CINFO + "[green]response: \"" + str(message))
            print(CSUCC + "Conversation is over.")
            print(CINFO + "Synthesizing response audio...")
            #print("Bobby: " + completion['message']['content'])
            #print(completion)
            audio = speak.save(completion['message']['content'])
            print(CSUCC + "Audio synthesized.")
            print(CINFO + audio)
            message = completion['message']
            #print(audio)
            return audio
            #voice_input = listen.listen()
            #print("User: " + voice_input)
            #message = {"role": "user", "content": voice_input}
        else:
            raise Exception("Invalid response type: not a function call or stop")

@app.route('/think')
def think():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Query parameter "q" is required'}), 400
    
    print(CINFO + "Got request.")
    print(CINFO + "[italic][green]\"" + query + "\"")

    # For demonstration purposes, let's just return the query itself.
    # You can replace this with any logic you want.
    response = {
        'query_received': query,
        'response': process(str(query))
    }
    return jsonify(response)

@app.route('/listen')
def listen():
    filepath = request.args.get('f')
    
    # Security measure to ensure arbitrary paths aren't accessed
    if '..' in filepath or filepath.startswith('/'):
        return jsonify({'error': 'Invalid file path'}), 400

    full_path = os.path.join('tmp', filepath)  # assuming 'audio_files' directory exists

    if not os.path.exists(full_path):
        return jsonify({'error': 'File not found'}), 404

    # Send the file with attachment mode so the browser can download or play it
    return send_file(full_path, as_attachment=True, attachment_filename=filepath, conditional=True)

if __name__ == '__main__':
    app.run(debug=True)
