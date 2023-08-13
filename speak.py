"""Synthesizes speech from a string using Elevenlabs Text-to-Speech API."""
from elevenlabs import generate, stream

class Speak:
    """Speak class"""
    def __init__(self, voice='Bella', api_key=None):
        """Initialize Speak class
        
        Args:
            voice: Voice name
            api_key: API key for Elevenlabs
        """
        self.voice = voice
        self.api_key = api_key

    def speak(self, text):
        """Speak text
        
        Args:
            text: Text to speak
        """
        audio = generate(
            text=text,
            voice=self.voice,
            api_key=self.api_key,
            stream=True
        )
        stream(audio)