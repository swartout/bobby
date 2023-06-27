# utility functions
import openai
import skills

class SkillHelper: # test stub class
    def __init__(self):
        self.skills = [skills.TurnLightsOn, skills.TurnLightsOff, skills.PlayMusic, skills.StopMusic]
    
    def getSkills(self):
        return {skill.name(): skill.description() for skill in self.skills}
    
    def doSkill(self, skill):
        # Iterate over the classes
        for s in self.skills:
            # Check if the class name matches
            if s.name() == skill:
                # Call the .doAction() method dynamically
                return getattr(s, "doSkill")()
        else:
            print(f"Class '{skill}' does not exist.")


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