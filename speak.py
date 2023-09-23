"""Synthesizes speech from a string using Elevenlabs Text-to-Speech API."""
from elevenlabs import generate, stream
import wave
import threading
import pyaudio
import pygame

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
        self.thinking = False
        self.think_thread = None
        pygame.init()
        pygame.mixer.init()
        
    def _play_think(self):
        """Private method to play think.mp3 in a loop using pyAudio."""
        chunk = 1024
        wf = wave.open('sound/think.wav', 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(chunk)

        while self.thinking and data:
            stream.write(data)
            data = wf.readframes(chunk)
            if not data:  # If file end is reached, loop from the beginning.
                wf.rewind()
                data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()

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

    def hearing(self):
        """Play a hearing sound"""
        pygame.mixer.music.load('sound/hearing.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def heard(self):
        """Play a heard sound"""
        pygame.mixer.music.load('sound/heard.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
    def think(self):
        """Play a think sound in a loop using a separate thread."""
        self.thinking = True
        self.think_thread = threading.Thread(target=self._play_think)
        self.think_thread.start()
        
    def stop_think(self):
        """Stop the think sound."""
        self.thinking = False
        if self.think_thread:
            self.think_thread.join()  # Wait for the thread to finish.
        pygame.mixer.music.load('sound/speak.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    
    def speaksnd(self):
        """Play a sound right before speaking"""
        pygame.mixer.music.load('sound/think.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    
    def done(self):
        """Play a done speaking sound"""
        pygame.mixer.music.load('sound/done.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)