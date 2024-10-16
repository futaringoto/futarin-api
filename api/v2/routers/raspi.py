import asyncio
import os
import tempfile
from typing import Any, List

from azure.messaging.webpubsubservice import WebPubSubServiceClient
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from httpx import HTTPStatusError, RequestError
from sqlalchemy.ext.asyncio import AsyncSession

import v2.cruds.raspi as raspi_crud
import v2.schemas.raspi as raspi_schema
from db import get_db
from v2.services.blob_storage import (
    get_blob_service_client,
    is_downloaded_blob,
    upload_blob_file,
)
from v2.services.gpt import generate_text
from v2.services.pubsub import (
    get_service,
    push_id_to_raspi_id,
    push_text,
    push_transcription,
)
from v2.services.voicevox_api import get_voicevox_audio
from v2.services.whisper import speech2text
from v2.utils.logging import get_logger
from v2.utils.query import get_user_by_raspi_id, get_user_paired_by_couple_id, get_thread_id

router = APIRouter()
logger = get_logger()

# azure-blob-storageの認証
blob_service_client = get_blob_service_client()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/{raspi_id}",
    tags=["futarin-raspi"],
    summary="返答の生成",
    response_class=FileResponse,
    responses={
        200: {
            "content": {"audio/wav": {"schema": {"type": "string", "format": "binary"}}}
        }
    },
)
async def all(
    raspi_id: int,
    file: UploadFile = File(...),
    speaker: int = 1,
    mode: int = 0,
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    try:
        get_user_task = asyncio.create_task(get_user_by_raspi_id(db, raspi_id))
        content: bytes = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        # whisper
        transcription: str = await speech2text(temp_file_path)
        logger.info(f"transcription: {transcription.text}")
        push_transcription(raspi_id, transcription.text)

        # chatgpt
        user = await get_user_task
        thread_id = user.thread_id
        generated_text: str = await generate_text(mode, thread_id, transcription.text)
        logger.info(f"generated text: {generated_text}")
        push_text(raspi_id, generated_text)

        # voicevox
        audio: bytes = await get_voicevox_audio(generated_text, speaker)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(audio)
    except (RequestError, HTTPStatusError) as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    return FileResponse(temp_file.name, media_type="audio/wav", filename="audio.wav")


@router.post(
    "/{raspi_id}/messages",
    tags=["futarin-raspi"],
    summary="メッセージ送信",
    response_model=raspi_schema.RaspiMessageResponse,
)
async def create_message(
    raspi_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
) -> Any:
    try:
        user = await get_user_by_raspi_id(db, raspi_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_paired = await get_user_paired_by_couple_id(db, user)
        if not user_paired:
            raise HTTPException(status_code=404, detail="Paired user not found")

        content: bytes = await file.read()
        # TODO raspi_idで登録している
        await upload_blob_file(raspi_id, blob_service_client, content)

        service: WebPubSubServiceClient = get_service()
        await push_id_to_raspi_id(
            service,
            receiver_raspi_id=user_paired.raspi_id,
            # TODO raspi_idで送信している
            sender_user_id=raspi_id,
        )
        return {"id": raspi_id, "message": "success"}
    except Exception as e:
        logger.error(f"Error occurred while processing the message: {e}")
        raise HTTPException(status_code=500, detail="An error occurred")


@router.post(
    "/{raspi_id}/negotiate", tags=["futarin-raspi"], summary="websocketsのURL発行"
)
async def negotiate(raspi_id: int):
    if not raspi_id:
        return "missing user id", 400
    service = get_service()
    token = service.get_client_access_token(user_id=raspi_id)
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


@router.get(
    "/raspi/{id}/name", tags=["raspis"], summary="ラズパイIDからラズパイの名前を取得"
)
async def get_raspi_name(id: int, db: AsyncSession = Depends(get_db)):
    return await raspi_crud.get_raspi_name(db, id)
