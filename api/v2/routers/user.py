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
    response_model=List[user_schema.User(couple_id=1)],
)
async def list_users():
    return [user_schema.User()]


@router.post(
    "/",
    tags=["users"],
    summary="新規ユーザの作成",
)
async def create_user():
    pass


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
