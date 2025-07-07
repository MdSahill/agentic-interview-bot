from openai import OpenAI
client = OpenAI()

def transcribe_audio(audiofile: str) -> str:
    with open(audiofile, "rb") as f:
        transcript = client.audio.transcriptions.create(
            file=f,
            model="whisper-1"
        )
    return transcript.text
