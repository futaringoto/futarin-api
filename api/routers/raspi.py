from typing import Any, Dict
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from services.gpt import generate_text
from services.voicevox import audio_query, synthesis
from services.whisper import speech2text
from httpx import RequestError, HTTPStatusError
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
async def audio(text: str, speaker: int = 1):
    try:
        query: Dict[str, Any] = await audio_query(text, speaker)
        content: bytes = await synthesis(query, speaker)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with open(temp_file.name, 'wb') as f:
            f.write(content)
    except RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
    except HTTPStatusError as e:
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

@router.post("/raspi/gpt")
async def gpt(text: str) -> JSONResponse:
    try:
        generated_text: str = generate_text(text)
        return JSONResponse(
            content={"generatedText": generated_text},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
