import os

from fastapi import APIRouter, File, HTTPException, UploadFile

from v1.schemas.sandbox import TextResponse
from v1.services.gpt import generate_text
from v1.services.whisper import speech2text

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/transcript",
    tags=["sandbox"],
    summary="whisperによる文字起こし",
    response_model=TextResponse,
)
async def transcript(file: UploadFile = File(...)) -> TextResponse:
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    try:
        content: bytes = await file.read()
        with open(file_location, "wb") as f:
            f.write(content)
        transcription: str = speech2text(file_location)
        os.remove(file_location)

        return TextResponse(text=transcription.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/gpt",
    tags=["sandbox"],
    summary="chatGPTによる文章生成",
    response_model=TextResponse,
)
async def gpt(text: str) -> TextResponse:
    try:
        generated_text: str = generate_text(text)
        return TextResponse(text=generated_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
