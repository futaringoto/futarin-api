import os
import tempfile
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from httpx import HTTPStatusError, RequestError
from sqlalchemy.ext.asyncio import AsyncSession

import v2.schemas.raspi as raspi_schema
from db import get_db
from v1.services.voicevox_api import get_voicevox_audio
from v1.services.whisper import speech2text
from v1.utils.logging import get_logger
from v2.azure.storage import (
    download_blob_file,
    get_blob_storage_account,
    upload_blob_file,
)
from v2.services.gpt import generate_text
from v2.utils.query import get_thread_id, get_user_id_same_couple

router = APIRouter()
logger = get_logger()

# azureの認証
blob_service_client = get_blob_storage_account()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/{id}",
    tags=["raspi"],
    summary="一連の動作全て",
    response_class=FileResponse,
    responses={
        200: {
            "content": {"audio/wav": {"schema": {"type": "string", "format": "binary"}}}
        }
    },
)
async def all(
    id: int,
    file: UploadFile = File(...),
    speaker: int = 1,
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    try:
        print(id)
        # whisper
        content: bytes = await file.read()
        with open(file_location, "wb") as f:
            f.write(content)
        transcription: str = speech2text(file_location)
        os.remove(file_location)
        logger.info(f"transcription: {transcription.text}")

        # chatgpt
        thread_id = await get_thread_id(db, id)
        generated_text: str = generate_text(thread_id, transcription.text)
        logger.info(f"generated text: {generated_text}")

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


@router.post(
    "/{id}/messages",
    tags=["raspi"],
    summary="メッセージ送信",
    response_model=raspi_schema.RaspiMessageResponse,
)
async def create_message(
    id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
) -> Any:
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    content: bytes = await file.read()
    with open(file_location, "wb") as f:
        f.write(content)

    with open(file_location, "rb") as data:
        response = await upload_blob_file(id, blob_service_client, db, data)
    os.remove(file_location)

    return response


@router.get(
    "/{id}",
    tags=["raspi"],
    summary="同coupleのメッセージ取得",
    response_model=raspi_schema.RaspiMessageResponse,
)
async def get_message(id: int, db: AsyncSession = Depends(get_db)):
    # 同coupleのidを取得
    boddy_id = await get_user_id_same_couple(db, id)
    # 同coupleのファイルをダウンロード
    response = download_blob_file(id, str(boddy_id), blob_service_client)
    return response
