from openai import OpenAI

from utils.config import get_openai_api_key

OpenAI.api_key = get_openai_api_key()
client = OpenAI()


def text2speech(text: str) -> bytes:
    res = client.audio.speech.create(
        model="tts-1", voice="shimmer", input=text, response_format="wav"
    )
    return res.content
