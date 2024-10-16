from openai import AsyncOpenAI

from v1.utils.config import get_openai_api_key

AsyncOpenAI.api_key = get_openai_api_key()
client = AsyncOpenAI()


async def speech2text(file_location: str) -> str:
    audio_file = open(file_location, "rb")
    transcription = await client.audio.transcriptions.create(
        model="whisper-1", file=audio_file, response_format="json", language="ja"
    )
    return transcription
