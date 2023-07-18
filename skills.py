from utils import Skill

class TurnLightsOn(Skill):
    def name(self):
        return "TurnLightsOn"

    def description(self):
        return "Turns the lights on to full brightness in the room."
    
    def do_skill(self):
        return "Turning lights on"

class TurnLightsOff(Skill):
    def name(self):
        return "TurnLightsOff"

    def description(self):
        return "Turns the lights off in the room."
    
    def do_skill(self):
        return "Turning lights off"

class PlayMusic(Skill):
    def name(self):
        return "PlayMusic"

    def description(self):
        return "Plays music from a playlist."
    
    def do_skill(self):
        return "Playing music"

class StopMusic(Skill):
    def name(self):
        return "StopMusic"

    def description(self):
        return "Stops playing music."
    
    def do_skill(self):
        return "Error stopping music - music was not playing"