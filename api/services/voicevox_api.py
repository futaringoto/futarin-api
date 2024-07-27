import httpx
from utils.config import get_voicevox_api_key

url: str = "https://deprecatedapis.tts.quest/v2/voicevox/audio/"
API_KEY = get_voicevox_api_key()

async def get_voicevox_audio(text: str, speaker: int) -> bytes:
    async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
        params = {"text": text, "speaker": speaker, "key": API_KEY}
        res = await client.post(
            url,
            params=params
        )
        res.raise_for_status()
        content: bytes = res.content
        return content
