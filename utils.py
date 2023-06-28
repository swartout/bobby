# utility functions
import openai
import skills
import os
import json
import subprocess

class Skill:
    def __init__(self, path):
        with open(path) as f:
            skillData = json.load(f)
            self.skillName = path.replace("skills/", "").replace("/skill.json","")
            self.skillDescription = skillData["description"]
            self.skillScript = path.replace("skill.json", skillData["script"])
            self.skillParameters = skillData["parameters"]
    
    def name(self):
        return self.skillName
        
    def description(self):
        return self.skillDescription
    
    def parameters(self):
        return self.skillParameters
    
    def execute(self, arguments):
        if self.parameters() != "readonly":
            args = ' '.join([f'--{key}={value}' for key, value in arguments.items()])
            subprocess_list = ["python", self.skillScript]
            for arg in args.split(" "):
                subprocess_list.append(arg)
            return subprocess.check_output(subprocess_list).decode().strip()
            #raise Exception("Skill " + self.name() + " requires parameters, but none given. (Accessor called as if mutator)")
        else:
            return subprocess.check_output(["python", self.skillScript, "--get"]).decode().strip()
    
    def openaiFunc(self):
        function_dict = {
            "name": self.skillName.replace(" ", "_").lower(),  # function names usually don't have spaces
            "description": self.skillDescription,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }

        if self.parameters() == "readonly":
            return function_dict

        for param in self.parameters():
            param_name = param["name"]
            function_dict["parameters"]["properties"][param_name] = {
                "description": param["description"]
            }

            if "range" in param:
                # if the parameter's range is a list of string options
                if isinstance(param["range"], list) and all(isinstance(i, str) for i in param["range"]):
                    function_dict["parameters"]["properties"][param_name]["type"] = "string"
                    function_dict["parameters"]["properties"][param_name]["enum"] = param["range"]
                # if the parameter's range is an integer range
                elif isinstance(param["range"], list) and len(param["range"]) == 2 and all(isinstance(i, int) for i in param["range"]):
                    function_dict["parameters"]["properties"][param_name]["type"] = "integer"
                    function_dict["parameters"]["properties"][param_name]["minimum"] = param["range"][0]
                    function_dict["parameters"]["properties"][param_name]["maximum"] = param["range"][1]

            if param.get("required", False):
                function_dict["parameters"]["required"].append(param_name)

        return function_dict

class SkillHelper: # test stub class
    def __init__(self):
        self.skills = []
        skillDirs = os.listdir("skills")
        for skill in skillDirs:
            self.skills.append(Skill("skills/" + skill + "/skill.json"))
    
    def getSkills(self):
        return {skill.name(): skill.description() for skill in self.skills}
    
    def doSkill(self, skill, arguments):
        for s in self.skills:
            if s.name() == skill:
                return s.execute(arguments)
        else:
            print(f"Class '{skill}' does not exist.")
    
    def gatherFunctions(self):
        functions_list = []
        for s in self.skills:
            functions_list.append(s.openaiFunc())
        return functions_list

# DEPRECATED - See SkillHelper.gatherFunctions()
def get_func(name, description):
    """Formats a skill into a function for OpenAI's API.
    
    Args:
        name: The name of the skill.
        description: The description of the skill.
    
    Returns:
        A dictionary representing the skill as a function, formatted for OpenAI's API.
    """
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": {},
        },
    }


def get_completion(messages, functions, model):
    """Gets a completion from OpenAI's API.
    
    Args:
        messages: A list of messages to send to the API.
        functions: A list of functions to send to the API.
        model: The model to use for the API.
        
    Returns:
        An OpenAI completion."""
    return openai.ChatCompletion.create(
        model=model,
        messages=messages,
        functions=functions
    )['choices'][0]


SYSTEM_MESSAGE = {
    "role": "system",
    "content":
"""You are a helpful home assistant named Bobby. You will have access to skills,
real-world actions you can take to help your user.  These skills come in the
form of functions which will be provided to you. Do not use a function unless it
perfectly matches the user's request. If you are unsure, further ask the user
what skill to use. Do not guess or assume what to use as function parameters, if
it is not obvious ask the user for clarification.  When calling a function, do
NOT pass any arguments unless they are defined in the function's parameters.""",
}