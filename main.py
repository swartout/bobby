import os
import json
import openai
from bobby import Bobby
from speak import Speak
from listen import Listen
from utils import SkillHelper, SYSTEM_MESSAGE
import pvporcupine
from pvrecorder import PvRecorder
from rich.console import Console

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

console = Console()

recorder = PvRecorder(device_index=-1, frame_length=512)

listen = Listen(API_KEY)
    
skill_helper = SkillHelper(SKILLS)
bobby = Bobby(SYSTEM_MESSAGE, skill_helper.get_skills(), MODEL)
speak = Speak()

while True:
    try:
        # wait for wake word
        console.log("Listening for wake word...")
        recorder.start()
        while True:
            pcm = recorder.read()
            keyword_index = ppn.process(pcm)
            if keyword_index >= 0:
                console.log("Wake word detected!")
                recorder.stop()
                break

        speak.hearing()
        messages = [SYSTEM_MESSAGE]

        # get user input
        console.log('Listening for user input...')
        voice_input = listen.listen()
        speak.heard()
        console.log("User: " + voice_input)
        message = {"role": "user", "content": voice_input}
        while True:
            speak.think()
            completion = bobby.get_response(message)
            speak.stop_think()  # Stop the think sound

            # do different things if response is chat vs function
            if completion['finish_reason'] == 'function_call':
                called_function_name = completion['message']["function_call"]["name"]
                called_function_args = completion['message']["function_call"]["arguments"]
                message = completion['message']
                params = json.loads(called_function_args)
                if called_function_name == "EndConversation":
                    console.log("Bobby: " + params['message'])
                    speak.speak(params['message'])
                console.log("Function call: " + called_function_name + ", Args: " + called_function_args)
                skill_info = skill_helper.do_skill(called_function_name, params=params)
                message = {"role": "function", "name": called_function_name, "content": skill_info}
                console.log("Function info: " + str(skill_info))
            elif completion['finish_reason'] == 'stop':
                console.log("Bobby: " + completion['message']['content'])
                console.log(completion)
                speak.speak(completion['message']['content'])
                speak.done()
                message = completion['message']
                speak.hearing()
                console.log('Listening for user input...')
                voice_input = listen.listen()
                console.log("User: " + voice_input)
                message = {"role": "user", "content": voice_input}
            else:
                raise Exception("Invalid response type: not a function call or stop")
    except Exception as e:
        console.log(f"Exception: {e}")