from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import v2.cruds.couple as couple_crud
import v2.schemas.couple as couple_schema
from db import get_db
from v2.utils.logging import get_logger

router = APIRouter()
logger = get_logger()


@router.get(
    "/",
    tags=["couples"],
    summary="ペアの取得",
    response_model=List[couple_schema.CoupleResponse],
)
async def list_couples(db: AsyncSession = Depends(get_db)):
    return await couple_crud.get_couples(db)


@router.post(
    "/",
    tags=["couples"],
    summary="新規ペアの作成",
    response_model=couple_schema.CoupleResponse,
)
async def create_couple(
    couple: couple_schema.CoupleCreate, db: AsyncSession = Depends(get_db)
):
    return await couple_crud.create_couple(db, couple)


@router.put(
    "/{id}",
    tags=["couples"],
    summary="ペアの更新",
    response_model=couple_schema.CoupleResponse,
)
async def update_couple(
    id: int, couple_body: couple_schema.CoupleUpdate, db: AsyncSession = Depends(get_db)
):
    couple = await couple_crud.get_couple(db, couple_id=id)
    if couple is None:
        raise HTTPException(status_code=404, detail="Couple not found")
    return await couple_crud.update_couple(db, couple_body, original=couple)


@router.delete(
    "/{id}",
    tags=["couples"],
    summary="ペアの削除",
)
async def delete_couple(id: int, db: AsyncSession = Depends(get_db)):
    couple = await couple_crud.get_couple(db, couple_id=id)
    if couple is None:
        raise HTTPException(status_code=404, detail="Couple not found")
    return await couple_crud.delete_couple(db, original=couple)
