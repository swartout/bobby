import os
import openai
from utils import get_func, get_completion, SkillHelper, SYSTEM_MESSAGE
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)

MODEL = "gpt-3.5-turbo-0613"
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise Exception("Missing OPENAI_API_KEY environment variable")
openai.api_key = api_key
    
skill_helper = SkillHelper()
skills_list = skill_helper.getSkills()
functions = skill_helper.gatherFunctions()
messages = [SYSTEM_MESSAGE]

##print("skills_list: " + str(skills_list))
##print("functions: " + str(functions))

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
        skill_info = skill_helper.doSkill(called_function_name, json.loads(called_function_args))
        messages.append({"role": "function", "name": called_function_name, "content": skill_info})
        print("Function info: " + str(skill_info))
    elif completion['finish_reason'] == 'stop':
        print("Bobby: " + completion['message']['content'])
        messages.append(completion['message'])
        print("User: ", end="")
        messages.append({"role": "user", "content": input()})
    else:
        raise Exception("Invalid response type: not a function call or stop")