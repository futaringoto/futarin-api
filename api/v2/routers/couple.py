from typing import List
from fastapi import APIRouter
from v2.utils.logging import get_logger
import v2.schemas.couple as couple_schema

router = APIRouter()
logger = get_logger()


@router.get(
    "/",
    tags=["couples"],
    summary="ペアの取得",
    response_model=List[couple_schema.CoupleResponse],
)
async def list_couples():
    return [couple_schema.CoupleResponse()]


@router.post(
    "/",
    tags=["couples"],
    summary="新規ペアの作成",
    response_model=couple_schema.CoupleResponse,
)
async def create_couple():
    pass


@router.put(
    "/{id}",
    tags=["couples"],
    summary="ペアの更新",
    response_model=couple_schema.CoupleResponse,
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
