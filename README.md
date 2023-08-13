# (Basic) Setup

- Install requirements using `pip install -r requirements.txt` (ideally in a virtual environment)
    - If you have a Mac, `pip install PyObjC` and `brew install portaudio` is also required
- Download a Picovoice Porcupine wake word model for the phrase "Hey Bobby" from
  [here](https://console.picovoice.ai/), unzip it, and rename it to
  `heybobby.ppn`. Place it in the directory.
- Add the following environment API KEYS
    - `export OPENAI_API_KEY=<your key>`
    - `export PORCUPINE_API_KEY=<your key>`
    - `export ELEVENLABS_API_KEY=<your key>`

You're all set!