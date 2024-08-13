from openai import OpenAI

from v1.utils.config import get_openai_api_key

OpenAI.api_key = get_openai_api_key()
client = OpenAI()


def speech2text(file_location: str) -> str:
    audio_file = open(file_location, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=audio_file, response_format="json", language="ja"
    )
    return transcription
