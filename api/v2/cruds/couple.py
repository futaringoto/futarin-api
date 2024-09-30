from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import v2.models.couple as couple_model
import v2.schemas.couple as couple_schema


async def create_couple(
    db: AsyncSession, couple_create: couple_schema.CoupleCreate
) -> couple_model.Couple:
    couple = couple_model.Couple(**couple_create.dict())
    db.add(couple)
    await db.commit()
    await db.refresh(couple)
    return couple


async def get_couples(db: AsyncSession):
    result: Result = await db.execute(
        select(
            couple_model.Couple.id,
            couple_model.Couple.name,
            couple_model.Couple.created_at,
            couple_model.Couple.updated_at,
        )
    )
    return result.all()


async def get_couple(db: AsyncSession, couple_id: int):
    result: Result = await db.execute(
        select(couple_model.Couple).filter(couple_model.Couple.id == couple_id)
    )
    couple = result.first()
    return couple[0] if couple is not None else None


async def update_couple(
    db: AsyncSession,
    couple_update: couple_schema.CoupleUpdate,
    original: couple_model.Couple,
) -> couple_model.Couple:
    original.name = couple_update.name
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_couple(db: AsyncSession, original: couple_model.Couple) -> None:
    await db.delete(original)
    await db.commit()
