from utils import Skill

class TurnLightsOn(Skill):
    def name():
        return "TurnLightsOn"

    def description():
        return "Turns the lights on to full brightness in the room."
    
    def do_skill():
        return "Turning lights on"

class TurnLightsOff(Skill):
    def name():
        return "TurnLightsOff"

    def description():
        return "Turns the lights off in the room."
    
    def do_skill():
        return "Turning lights off"

class PlayMusic(Skill):
    def name():
        return "PlayMusic"

    def description():
        return "Plays music from a playlist."
    
    def do_skill():
        return "Playing music"

class StopMusic(Skill):
    def name():
        return "StopMusic"

    def description():
        return "Stops playing music."
    
    def do_skill():
        return "Stopping music"