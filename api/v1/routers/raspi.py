import os
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from httpx import HTTPStatusError, RequestError

from v1.services.gpt import generate_text
from v1.services.voicevox_api import get_voicevox_audio
from v1.services.whisper import speech2text
from v1.utils.audio_converter import wav2mp3
from v1.utils.logging import get_logger

router = APIRouter()
logger = get_logger()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/",
    tags=["raspi"],
    summary="一連の動作全て",
    response_class=FileResponse,
    responses={
        200: {
            "content": {"audio/wav": {"schema": {"type": "string", "format": "binary"}}}
        }
    },
)
async def all(speaker: int = 1, file: UploadFile = File(...)) -> FileResponse:
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    try:
        # whisper
        content: bytes = await file.read()
        with open(file_location, "wb") as f:
            f.write(content)
        transcription: str = speech2text(file_location)
        os.remove(file_location)
        logger.info(f"transcription: {transcription.text}")

        # chatgpt
        generated_text: str = generate_text(transcription.text)
        logger.info(f"generated text: {generated_text}")

        audio: bytes = await get_voicevox_audio(generated_text, speaker)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
            tmp_wav_path = tmp_wav.name
            with open(tmp_wav_path, "wb") as f:
                f.write(audio)

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_mp3:
            tmp_mp3_path = tmp_mp3.name

        # temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        # with open(tmp_wav_path, "wb") as f:
        #    f.write(audio)
        print(f"tmp_wav_path: {tmp_wav_path} exist: {os.path.isfile(tmp_wav_path)}")
        print(f"tmp_mp3_path: {tmp_mp3_path} exist: {os.path.isfile(tmp_mp3_path)}")
        wav2mp3(tmp_wav_path, tmp_mp3_path)
        return FileResponse(tmp_mp3_path, media_type="audio/mp3", filename="audio.mp3")

    except RequestError as e:
        raise HTTPException(
            status_code=500, detail=f"RequestError fetching data: {str(e)}"
        )
    except HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=f"Error fetching data: {str(e)}"
        )
    # finally:
    # os.remove(tmp_wav_path)
    # os.remove(tmp_mp3_path)
