import json
from typing import Any, Dict
import httpx
import urllib.parse
from utils.config import get_voicevox_url

url: str = get_voicevox_url()

async def audio_query(text: str, speaker: int) -> Dict[str, Any]:
    params = {"text": text, "speaker": speaker}
    async with httpx.AsyncClient() as client:
        res = await client.post(
            urllib.parse.urljoin(url, "/audio_query"),
            params=params
        )
        res.raise_for_status()
        query = res.json()
        return query

async def synthesis(query: Dict[str, Any], speaker: int) -> bytes:
    async with httpx.AsyncClient(timeout=httpx.Timeout(20.0)) as client:
        res = await client.post(
            urllib.parse.urljoin(url, "/synthesis"),
            params={"speaker": speaker},
            data=json.dumps(query),
            headers={"Content-Type": "application/json"}
        )
        res.raise_for_status()
        content: bytes = res.content
        return content


