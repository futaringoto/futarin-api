import os

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from v1.services.gpt import generate_text
from v1.services.whisper import speech2text

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/transcript", tags=["sandbox"], summary="whisperによる文字起こし")
async def transcript(file: UploadFile = File(...)) -> JSONResponse:
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    try:
        content: bytes = await file.read()
        with open(file_location, "wb") as f:
            f.write(content)
        transcription: str = speech2text(file_location)
        os.remove(file_location)

        return JSONResponse(content={"transcript": transcription.text}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.post("/gpt", tags=["sandbox"], summary="chatGPTによる文章生成")
async def gpt(text: str) -> JSONResponse:
    try:
        generated_text: str = generate_text(text)
        return JSONResponse(content={"generatedText": generated_text}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
