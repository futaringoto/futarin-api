from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import v2.schemas.user as user_schema
import v2.cruds.user as user_crud
from db import get_db
from v2.utils.logging import get_logger

router = APIRouter()
logger = get_logger()


@router.get(
    "/",
    tags=["users"],
    summary="ユーザの取得",
    response_model=List[user_schema.UserResponse],
)
async def list_users():
    return [user_schema.UserResponse()]


@router.post(
    "/",
    tags=["users"],
    summary="新規ユーザの作成",
    response_model=user_schema.UserResponse,
)
async def create_user(
    user: user_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    return await user_crud.create_user(db, user)
    
    # new_user = {
    #     "id": 1,
    #     "couple_id": user.couple_id,
    #     "name": user.name,
    #     "created_at": datetime.now(),
    #     "updated_at": datetime.now(),
    # }
    # return new_user


@router.put(
    "/{id}",
    tags=["users"],
    summary="ユーザの更新",
)
async def update_user(id: int, user: user_schema.UserUpdate):
    updated_user = {
        "id": id,
        "couple_id": user.couple_id,
        "name": user.name,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    return updated_user


@router.delete(
    "/{id}",
    tags=["users"],
    summary="ユーザの削除",
)
async def delete_user():
    pass
