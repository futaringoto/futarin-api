import json
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from services.whisper import speech2text
import httpx
import tempfile
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

@router.post("/raspi/transcript")
async def transcript(file: UploadFile = File(...)) -> JSONResponse:
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    try:
        content: bytes = await file.read()
        with open(file_location, "wb") as f:
            f.write(content)
        transcription: str = speech2text(file_location)
        os.remove(file_location)

        return JSONResponse(
            content={"transcript": transcription.text},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
