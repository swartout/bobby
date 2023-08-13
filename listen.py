"""Handles the speech-to-text transcription behavior"""
import speech_recognition as sr

class Listen:
    
    def __init__(self, api_key = None):
        self.api_key = api_key
    
    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("[DBG] Calibrating...")
            r.adjust_for_ambient_noise(source, duration=5)  
            r.dynamic_energy_threshold = True  
            print("[DBG] Listening...")
            audio = r.listen(source)
            return r.recognize_whisper_api(audio, api_key=api_key)
