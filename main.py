import os
import json
import openai
from bobby import Bobby
from speak import Speak
from listen import Listen
from utils import SkillHelper, SYSTEM_MESSAGE
import pvporcupine
from pvrecorder import PvRecorder

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

while True:
    # wait for wake word
    print("Listening for wake word...")
    recorder.start()
    while True:
        pcm = recorder.read()
        keyword_index = ppn.process(pcm)
        if keyword_index >= 0:
            print("Wake word detected!")
            recorder.stop()
            break

    speak.hearing()
    messages = [SYSTEM_MESSAGE]

    # get user input
    voice_input = listen.listen()
    speak.heard()
    print("User: " + voice_input)
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
                print("Bobby: " + params['message'])
                speak.speak(params['message'])
                break
            print("Function call: " + called_function_name + ", Args: " + called_function_args)
            skill_info = skill_helper.do_skill(called_function_name, params=params)
            message = {"role": "function", "name": called_function_name, "content": skill_info}
            print("Function info: " + str(skill_info))
        elif completion['finish_reason'] == 'stop':
            print("Bobby: " + completion['message']['content'])
            print(completion)
            speak.speak(completion['message']['content'])
            speak.done()
            message = completion['message']
            speak.hearing()
            voice_input = listen.listen()
            print("User: " + voice_input)
            message = {"role": "user", "content": voice_input}
        else:
            raise Exception("Invalid response type: not a function call or stop")