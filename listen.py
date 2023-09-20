"""Handles the speech-to-text transcription behavior"""
import speech_recognition as sr

class Listen:
    
    """Calibrate the microphone"""
    def __init__(self, api_key = None):
        self.api_key = api_key
        r = sr.Recognizer()
    
    """Transcribe some text"""
    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening!")
            audio = r.listen(source)
            return r.recognize_whisper_api(audio, api_key=self.api_key)