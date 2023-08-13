from utils import Skill

class EndConversation(Skill):
    def description(self):
        return """Ends the conversation. Use when the user's request has been fulfilled
        and the conversation is over. The parameter message is the last thing spoken to
        the user. Keep it brief."""
    
    def do_skill(self, message):
        return "Ending conversation"

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