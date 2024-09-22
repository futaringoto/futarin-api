from datetime import datetime
from fastapi import APIRouter
from typing import List
from v2.utils.logging import get_logger
import v2.schemas.user as user_schema

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
async def create_user(user: user_schema.UserCreate):
    new_user = {
        "id": 1,
        "couple_id": user.couple_id,
        "user_name": user.username,
        "create_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    return new_user


@router.put(
    "/{id}",
    tags=["users"],
    summary="ユーザの更新",
)
async def update_user():
    pass


@router.delete(
    "/{id}",
    tags=["users"],
    summary="ユーザの削除",
)
async def delete_user():
    pass
