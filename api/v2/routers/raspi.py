import os
import tempfile
from typing import Any, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from httpx import HTTPStatusError, RequestError
from sqlalchemy.ext.asyncio import AsyncSession

import v2.cruds.raspi as raspi_crud
import v2.schemas.raspi as raspi_schema
from db import get_db
from v1.services.voicevox_api import get_voicevox_audio
from v1.services.whisper import speech2text
from v1.utils.logging import get_logger
from v2.azure.storage import (
    get_blob_storage_account,
    is_downloaded_blob,
    upload_blob_file,
)
from v2.services.gpt import generate_text
from v2.services.pubsub import get_service, push_text, push_transcription
from v2.utils.query import get_thread_id

router = APIRouter()
logger = get_logger()

# azure-blob-storageの認証
blob_service_client = get_blob_storage_account()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/{id}",
    tags=["futarin-raspi"],
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
        push_transcription(id, transcription.text)

        # chatgpt
        thread_id = await get_thread_id(db, id)
        generated_text: str = generate_text(thread_id, transcription.text)
        logger.info(f"generated text: {generated_text}")
        push_text(id, generated_text)

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
    tags=["futarin-raspi"],
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
        response = await upload_blob_file(id, blob_service_client, data)
    os.remove(file_location)
    return response


@router.post("/{id}/negotiate", tags=["futarin-raspi"], summary="websocketsのURL発行")
async def negotiate(id: int):
    if not id:
        return "missing user id", 400
    service = get_service()
    token = service.get_client_access_token(user_id=id)
    return {"url": token["url"]}


@router.get(
    "/{raspi_id}/messages/{message_id}",
    tags=["futarin-raspi"],
    summary="同coupleのメッセージ取得",
    # response_model=Union[FileResponse, raspi_schema.RaspiMessageResponse],
)
async def get_message(
    raspi_id: int,
    message_id: int,
):
    # 同coupleのidを取得
    # boddy_id = await get_user_id_same_couple(db, id)
    # 同coupleのファイルをダウンロード
    is_downloaded = is_downloaded_blob(str(message_id), blob_service_client)

    if is_downloaded:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, f"../../downloads/{message_id}.wav")
        return FileResponse(
            path=file_path, media_type="audio/wav", filename=f"{message_id}.wav"
        )

    return {"id": raspi_id, "message": "相方のファイルは見つかりませんでした"}


@router.get(
    "/",
    tags=["raspis"],
    summary="ラズパイ一覧の取得",
    response_model=List[raspi_schema.RaspiResponse],
)
async def list_raspi(db: AsyncSession = Depends(get_db)):
    return await raspi_crud.get_raspis(db)


@router.post(
    "/",
    tags=["raspis"],
    summary="新規ラズパイの作成",
    response_model=raspi_schema.RaspiResponse,
)
async def create_raspi(
    raspi: raspi_schema.RaspiCreate, db: AsyncSession = Depends(get_db)
):
    return await raspi_crud.create_raspi(db, raspi)


@router.put(
    "/{id}",
    tags=["raspis"],
    summary="ラズパイの更新",
    response_model=raspi_schema.RaspiResponse,
)
async def update_raspi(
    id: int, raspi_body: raspi_schema.RaspiUpdate, db: AsyncSession = Depends(get_db)
):
    raspi = await raspi_crud.get_raspi(db, raspi_id=id)
    if raspi is None:
        raise HTTPException(status_code=404, detail="Raspi not found")
    return await raspi_crud.update_raspi(db, raspi_body, original=raspi)


@router.delete("/{id}", tags=["raspis"], summary="ラズパイの削除", response_model=None)
async def delete_raspi(id: int, db: AsyncSession = Depends(get_db)):
    raspi = await raspi_crud.get_raspi(db, raspi_id=id)
    if raspi is None:
        raise HTTPException(status_code=404, detail="Raspi not found")
    return await raspi_crud.delete_raspi(db, raspi)
