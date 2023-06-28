import openai
from abc import ABC, abstractmethod
import importlib

class Skill(ABC):
    """An Abstract Base Class for a skill that the virtual assistant can use.
    Users must subclass Skill to create their own skills for the virtual assistant.
    These skills should be placed in the skills.py file.

    i.e.
    
    class TurnLightsOff(Skill):
        def name(self):
            return "TurnLightsOff"

        def description(self):
            return "Turns the lights completly off in the main bedroom."

        def doSkill(self):
            # turn the lights off here!
            return "The lights have been successfully turned off"
    """

    @abstractmethod
    def name(self):
        """Gets the name of this Skill function.
        
        Returns:
            The name of this Skill
        """
        pass

    @abstractmethod
    def description(self):
        """A description of this Skill function.
        
        Returns:
            A description of this Skill
        """
        pass

    @abstractmethod
    def do_skill(self):
        """Runs this skill.
        
        Returns:
            A string representing the outcome of this running this skill.  For
            example, this could be a success, error, or state message.
        """
        pass


class SkillHelper:
    """Utility class for managing Skills"""

    def __init__(self, skills):
        """Construct a new SkillHelper.
        
        Args:
            skills: a list of strings representing the names of skill classes
                    i.e.  ['TurnLightsOn', 'TurnLightsOff', 'PlayMusic']
        """
        self.skills = []
        s = importlib.import_module('skills')
        for skill_name in skills:
            skill = getattr(s, skill_name)
            if not issubclass(skill, Skill):
                raise Exception(f'Skill: {skill_name} does not subclass Skill')
            new_skill = skill()
            self.skills.append(skill)
    
    def do_skill(self, skill, params={}):
        """Run a skill.
        
        Args:
            skill: the string function name of the skill to be run
            params: (optional) a dictionary mapping parameter names to values
        """
        for s in self.skills:
            if s.name() == skill:
                # TODO: implement better argument parsing
                return s.do_skill(**params)
        raise Exception('Skill name: {skill} not found')

    def get_skills(self):
        """Get all skills formatted as OpenAI functions.
        
        Returns:
            A dictionary of all skills formatted as OpenAI functions
        """
        # TODO: for now, I'm not supporting parameters in functions
        skill_funcs = []
        for s in self.skills:
            skill_funcs.append({
                    "name": s.name(),
                    "description": s.description(),
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                })
        return skill_funcs


def get_completion(messages, functions, model):
    """Gets a completion from OpenAI's API.
    
    Args:
        messages: A list of messages to send to the API.
        functions: A list of functions to send to the API.
        model: The model to use for the API.
        
    Returns:
        An OpenAI completion.
    """
    if len(functions) != 0:
        return openai.ChatCompletion.create(
            model=model,
            messages=messages,
            functions=functions
        )['choices'][0]
    else:
        return openai.ChatCompletion.create(
            model=model,
            messages=messages,
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