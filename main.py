import os
import openai
from utils import get_completion, SkillHelper, SYSTEM_MESSAGE

# ----------------------------------- CONFIG --------------------------- #

# the model to use - it should be one trained on function calling
MODEL = "gpt-3.5-turbo-0613"

# OpenAI API key - if left None, API_KEY will be the env variable OPENAI_API_KEY
API_KEY = None 

# list of skill names (string) to allow the virtual assistant to use, these
# skills must be placed in the skills.py file and subclass utils.Skill
SKILLS = [
    'TurnLightsOff',
    'TurnLightsOn',
    'PlayMusic',
    'StopMusic'
]

# ----------------------------------- CONFIG --------------------------- #


if API_KEY is None:
    API_KEY = os.getenv("OPENAI_API_KEY")
    if API_KEY is None:
        raise Exception("Missing OPENAI_API_KEY environment variable and none provided in config")
openai.api_key = API_KEY
    
skill_helper = SkillHelper(SKILLS)
functions = skill_helper.get_skills()
messages = [SYSTEM_MESSAGE]

# get user input
print("User: ", end="")
messages.append({"role": "user", "content": input()})

while True:
    completion = get_completion(messages, functions, MODEL)

    # do different things if response is chat vs function
    if completion['finish_reason'] == 'function_call':
        called_function_name = completion['message']["function_call"]["name"]
        called_function_args = completion['message']["function_call"]["arguments"]
        print("Function call: " + called_function_name + ", Args: " + called_function_args)
        messages.append(completion['message'])
        skill_info = skill_helper.do_skill(called_function_name)
        messages.append({"role": "function", "name": called_function_name, "content": skill_info})
        print("Function info: " + str(skill_info))
    elif completion['finish_reason'] == 'stop':
        print("Bobby: " + completion['message']['content'])
        messages.append(completion['message'])
        print("User: ", end="")
        messages.append({"role": "user", "content": input()})
    else:
        raise Exception("Invalid response type: not a function call or stop")