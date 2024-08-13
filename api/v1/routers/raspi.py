import os
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from httpx import HTTPStatusError, RequestError

from v1.services.gpt import generate_text
from v1.services.voicevox_api import get_voicevox_audio
from v1.services.whisper import speech2text

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/",
    tags=["raspi"],
    summary="一連の動作全て",
    response_class=FileResponse,
    responses={
        200: {
            "content": {
                "audio/wav": {"schema": {"type": "string", "format": "binary"}}
            }
        }
    }
)
async def all(speaker: int = 1, file: UploadFile = File(...)) -> JSONResponse:
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    try:
        # whisper
        content: bytes = await file.read()
        with open(file_location, "wb") as f:
            f.write(content)
        transcription: str = speech2text(file_location)
        os.remove(file_location)
        print(f"transcription: {transcription.text}")

        # chatgpt
        generated_text: str = generate_text(transcription.text)
        print(f"generated text: {generated_text}")

        audio: bytes = await get_voicevox_audio(generated_text, speaker)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with open(temp_file.name, "wb") as f:
            f.write(audio)
    except RequestError as e:
        raise HTTPException(
            status_code=500, detail=f"RequestError fetching data: {str(e)}"
        )
    except HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=f"Error fetching data: {str(e)}"
        )
    return FileResponse(temp_file.name, media_type="audio/wav", filename="audio.wav")
