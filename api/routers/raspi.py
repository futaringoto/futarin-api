import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import httpx
import tempfile
import os

router = APIRouter()

@router.post(
    "/raspi/audio",
    tags=["voicevox クエリ作成"],
    summary="音声合成用のクエリを作成する"
)
async def audio(
    text: str,
    speaker: int = 1,
):
    try:
        url = os.getenv("VOICEVOX_URL")
        params = {"text": text, "speaker": speaker}

        async with httpx.AsyncClient() as client:
            res1 = await client.post(
                url + "/audio_query",
                params=params
            )
            res1.raise_for_status()
            query = res1.json()

            res2 = await client.post(
                url + "/synthesis",
                params={"speaker": speaker},
                data=json.dumps(query),
                headers={"Content-Type": 'application/json'}
            )
            res2.raise_for_status()

            # 一時ファイル作成
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            with open(temp_file.name, 'wb') as f:
                f.write(res2.content)

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching data: {str(e)}")

    return FileResponse(
        temp_file.name,
        media_type="audio/wav",
        filename="audio.wav"
    )

