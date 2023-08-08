from utils import Skill

class TurnLightsOn(Skill):
    def description(self):
        return "Turns the lights on to full brightness in the room."
    
    def do_skill(self):
        return "Turning lights on"

    def get_state(self):
        return "Lights are disconnected"

class TurnLightsOff(Skill):
    def description(self):
        return "Turns the lights off in the room."
    
    def do_skill(self):
        return "Turning lights off"

    def get_state(self):
        return "Lights are off"

class PlayMusic(Skill):
    def description(self):
        return "Plays music from a playlist."
    
    def do_skill(self):
        return "Playing music"

class StopMusic(Skill):
    def description(self):
        return "Stops playing music."
    
    def do_skill(self):
        return "Error stopping music - music was not playing"