from fastapi import APIRouter
from v2.utils.logging import get_logger

router = APIRouter()
logger = get_logger()


@router.get(
    "/",
    tags=["couples"],
    summary="ペアの取得",
)
async def list_couples():
    pass


@router.post(
    "/",
    tags=["couples"],
    summary="新規ペアの作成",
)
async def create_couple():
    pass


@router.put(
    "/{id}",
    tags=["couples"],
    summary="ペアの更新",
)
async def update_couple():
    pass


@router.delete(
    "/{id}",
    tags=["couples"],
    summary="ペアの削除",
)
async def delete_couple():
    pass
