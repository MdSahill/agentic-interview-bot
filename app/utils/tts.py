import requests
import base64
import os
from murf import Murf
from IPython.display import Audio

ELEVEN_API_KEY = "ap2_fa3bf82d-c6fe-4330-8d15-460f74c6ff7c"
ELEVEN_VOICE_ID = os.getenv("ELEVEN_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # default voice

def synthesize_speech(text: str) -> str:
    client = Murf(api_key=ELEVEN_API_KEY)
    response = client.text_to_speech.generate(
        text = text,
        voice_id = "en-US-natalie"
    )
    # download the MP3 bytes from the URL
    mp3_data = requests.get(response.audio_file).content
    # encode to base64
    audio_b64 = base64.b64encode(mp3_data).decode("utf-8")
    return audio_b64
