from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import v2.models.raspi as raspi_model
import v2.schemas.raspi as raspi_schema
from v2.utils.logging import get_logger

logger = get_logger()


async def create_raspi(
    db: AsyncSession, raspi_create: raspi_schema.RaspiCreate
) -> raspi_model.Raspi:
    raspi = raspi_model.Raspi(**raspi_create.model_dump())
    db.add(raspi)
    await db.commit()
    await db.refresh(raspi)
    return raspi


async def get_raspis(db: AsyncSession):
    result: Result = await db.execute(
        select(
            raspi_model.Raspi.id,
            raspi_model.Raspi.name,
            raspi_model.Raspi.created_at,
            raspi_model.Raspi.updated_at,
        )
    )
    return result.all()


async def get_raspi(db: AsyncSession, raspi_id: int):
    result: Result = await db.execute(
        select(raspi_model.Raspi).filter(raspi_model.Raspi.id == raspi_id)
    )
    raspi = result.first()
    return raspi[0] if raspi is not None else None


async def update_raspi(
    db: AsyncSession,
    raspi_update: raspi_schema.RaspiUpdate,
    original: raspi_model.Raspi,
) -> raspi_model.Raspi:
    original.name = raspi_update.name
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_raspi(db: AsyncSession, original: raspi_model.Raspi) -> None:
    await db.delete(original)
    await db.commit()


async def update_ws_active(
    is_active: bool,
    db: AsyncSession,
    raspi: raspi_model.Raspi,
):
    raspi.ws_active = is_active
    db.add(raspi)
    await db.commit()
