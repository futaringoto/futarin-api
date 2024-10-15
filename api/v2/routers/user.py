from typing import List

from azure.storage.blob import BlobServiceClient
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import v2.cruds.user as user_crud
import v2.schemas.user as user_schema
from config import get_azure_sas_token, get_azure_storage_account
from db import get_db
from v2.services.gpt import create_new_thread_id, delete_thread_id
from v2.utils.logging import get_logger

router = APIRouter()
logger = get_logger()

# azureの認証
azure_storage_account = get_azure_storage_account()
account_url = f"https://{azure_storage_account}.blob.core.windows.net"
sas_token = get_azure_sas_token()
blob_service_client = BlobServiceClient(account_url, credential=sas_token)


@router.get(
    "/",
    tags=["users"],
    summary="ユーザの取得",
    response_model=List[user_schema.UserResponse],
)
async def list_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_users(db)


@router.post(
    "/",
    tags=["users"],
    summary="新規ユーザの作成",
    response_model=user_schema.UserResponse,
)
async def create_user(user: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        thread_id = await create_new_thread_id()
        user_result = await user_crud.create_user(db, user, thread_id)
        return user_result
    except user_crud.ForeignKeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/{id}",
    tags=["users"],
    summary="ユーザの更新",
)
async def update_user(
    id: int, user_body: user_schema.UserUpdate, db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_user(db, user_id=id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_crud.update_user(db, user_body, original=user)


@router.delete(
    "/{id}",
    tags=["users"],
    summary="ユーザの削除",
)
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user(db, user_id=id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await delete_thread_id(user.thread_id)
    return await user_crud.delete_user(db, user)
