# skills for bobby to use
# current skills are:
#  - TurnLightsOn
#  - TurnLightsOff
#  - PlayMusic
#  - StopMusic

# TODO: change all prints to logging

class TurnLightsOn:
    def name():
        return "TurnLightsOn"

    def description():
        return "Turns the lights on to full brightness in the room."
    
    def doSkill():
        return "Turning lights on"

class TurnLightsOff:
    def name():
        return "TurnLightsOff"

    def description():
        return "Turns the lights off in the room."
    
    def doSkill():
        return "Turning lights off"

class PlayMusic:
    def name():
        return "PlayMusic"

    def description():
        return "Plays music from a playlist."
    
    def doSkill():
        return "Playing music"

class StopMusic:
    def name():
        return "StopMusic"

    def description():
        return "Stops playing music."
    
    def doSkill():
        return "Stopping music"
