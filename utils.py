# utility functions
import openai
from abc import ABC, abstractmethod
import importlib
from inspect import signature

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
    def description(self):
        """A description of this Skill function.

        This should explain what this Skill does, what parameters it takes, and
        what it returns. This description will be shown to the model when it is
        deciding what function to call.
        
        Returns:
            A description of this Skill
        """
        pass

    @abstractmethod
    def do_skill(self):
        """Runs this skill.
        
        When overriding this method you are encouraged to use type annotations
        to specify the types of the parameters. Optional values are also
        supported.  For now, no description is used for the parameters, this
        should be specified in the description method.
        
        Returns:
            A string representing the outcome of this running this skill.  For
            example, this could be a success, error, or state message.
        """
        pass

    def get_state(self):
        """Get the state of this skill.
        
        This method is called occasionally to get the state of this skill.  This
        state is then passed to the model when it is deciding what function to
        call.  This method is optional and is not called if not implemented.

        Returns:
            A string representing the state of this skill.
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
            self.skills.append(new_skill)
    
    def do_skill(self, skill, params={}):
        """Run a skill.
        
        Args:
            skill: the string function name of the skill to be run
            params: (optional) a dictionary mapping parameter names to values
        """
        for s in self.skills:
            if s.__class__.__name__ == skill:
                return s.do_skill(**params)
        raise Exception('Skill name: {skill} not found')

    def get_skills(self):
        """Get all skills formatted as OpenAI functions.
        
        Returns:
            A dictionary of all skills formatted as OpenAI functions
        """
        skill_funcs = []
        for s in self.skills:
            params = {}
            required = []
            sig = signature(s.do_skill)
            for key, value in sig.parameters.items():
                if value.default == value.empty:
                    required.append(key)
                if value.annotation != value.empty:
                    params[key] = {
                        "type": str(value.annotation),
                    }
                else:
                    params[key] = {}

            skill_funcs.append({
                    "name": s.__class__.__name__,
                    "description": s.description(),
                    "parameters": {
                        "type": "object",
                        "properties": params,
                        "required": required
                    },
                })
        return skill_funcs

    def get_state(self):
        """Get the state of all skills.
        
        Returns:
            A dictionary mapping skill names to their states
        """
        states = {}
        for s in self.skills:
            state = s.get_state()
            if state:
                states[s.__class__.__name__] = state
        return states


SYSTEM_MESSAGE = {
    "role": "system",
    "content":
"""You are a helpful home assistant named Bobby. You will have access to skills,
real-world actions you can take to help your user.  These skills come in the
form of functions which will be provided to you. Do not use a function unless it
perfectly matches the user's request. If you are unsure, further ask the user
what skill to use. Do not guess or assume what to use as function parameters, if
it is not obvious ask the user for clarification.  When calling a function, do
NOT pass any arguments unless they are defined in the function's parameters.
Remember to be concise. This will be spoken as speech and must not be longer than
one or two sentences. Never, EVER, repeat yourself.""",
}