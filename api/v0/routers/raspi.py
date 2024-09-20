import os
import tempfile
from typing import Any, Dict

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from httpx import HTTPStatusError, RequestError

from v0.services.gpt import generate_text
from v0.services.tts import text2speech
from v0.services.voicevox import audio_query, synthesis
from v0.services.voicevox_api import get_voicevox_audio
from v0.services.whisper import speech2text

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/raspi/", tags=["v0 (deprecated)"], summary="一連の動作全て")
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

        # voicevox
        # query: Dict[str, Any] = await audio_query(generated_text, speaker)
        # audio: bytes = await synthesis(query, speaker)
        # audio: bytes = text2speech(generated_text)
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


@router.post("/raspi/audio", tags=["v0 (deprecated)"], summary="VOICEVOXによる音声合成")
async def audio(text: str, speaker: int = 1):
    try:
        query: Dict[str, Any] = await audio_query(text, speaker)
        content: bytes = await synthesis(query, speaker)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with open(temp_file.name, "wb") as f:
            f.write(content)
    except RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
    except HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=f"Error fetching data: {str(e)}"
        )
    return FileResponse(temp_file.name, media_type="audio/wav", filename="audio.wav")


@router.post("/raspi/tts", tags=["v0 (deprecated)"], summary="OpenAI TTSによる音声合成")
async def tts(text):
    try:
        content: bytes = text2speech(text)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with open(temp_file.name, "wb") as f:
            f.write(content)
    except RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
    except HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=f"Error fetching data: {str(e)}"
        )
    return FileResponse(temp_file.name, media_type="audio/wav", filename="audio.wav")


@router.post(
    "/raspi/transcript", tags=["v0 (deprecated)"], summary="whisperによる文字起こし"
)
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


@router.post("/raspi/gpt", tags=["v0 (deprecated)"], summary="chatGPTによる文章生成")
async def gpt(text: str) -> JSONResponse:
    try:
        generated_text: str = generate_text(text)
        return JSONResponse(content={"generatedText": generated_text}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
