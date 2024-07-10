from openai import OpenAI
from utils.config import get_openai_api_key

OpenAI.api_key = get_openai_api_key()
client = OpenAI()

def speech2text(audio_file: bytes) -> str:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="json",
        language="ja"
    )
    return transcription
