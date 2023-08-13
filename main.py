import os
import json
import openai
from bobby import Bobby
from speak import Speak
from listen import Listen
from utils import SkillHelper, SYSTEM_MESSAGE

# ---------------------------------- CONFIG ---------------------------------- #

# the model to use - it should be one trained on function calling
MODEL = "gpt-3.5-turbo-0613"

# OpenAI API key - if left None, API_KEY will be the env variable OPENAI_API_KEY
API_KEY = None 

# list of skill names (string) to allow the virtual assistant to use, these
# skills must be placed in the skills.py file and subclass utils.Skill
SKILLS = [
    'EndConversation',
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
    
skill_helper = SkillHelper(SKILLS)
bobby = Bobby(SYSTEM_MESSAGE, skill_helper.get_skills(), MODEL)
speak = Speak()
listen = Listen(API_KEY)
messages = [SYSTEM_MESSAGE]

# get user input
print("User: ", end="")
message = {"role": "user", "content": input()}

while True:
    completion = bobby.get_response(message)
    
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
        speak.speak(completion['message']['content'])
        message = completion['message']
        print("User: ", end="")
        message = {"role": "user", "content": input()}
    else:
        raise Exception("Invalid response type: not a function call or stop")