from fastapi import APIRouter
from v2.utils.logging import get_logger

router = APIRouter()
logger = get_logger()


@router.get(
    "/",
    tags=["users"],
    summary="ユーザの取得",
)
async def list_users():
    pass


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
