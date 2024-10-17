from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

import v2.models.user as user_model


async def get_user_by_raspi_id(db: Session, raspi_id: int) -> user_model.User:
    result = await db.execute(
        select(user_model.User).where(user_model.User.raspi_id == raspi_id)
    )
    return result.scalars().first()


async def get_user_paired_by_couple_id(
    db: Session, user: user_model.User
) -> user_model.User:
    result = await db.execute(
        select(user_model.User).where(user_model.User.couple_id == user.couple_id)
    )
    paired_users = result.scalars().all()
    for user_paired in paired_users:
        if user_paired.id != user.id:
            return user_paired


async def get_user_id_same_couple(db: AsyncSession, user_id: int):
    subquery = (
        select(user_model.User.couple_id)
        .where(user_model.User.id == user_id)
        .scalar_subquery()
    )
    stmt = select(user_model.User).where(user_model.User.couple_id == subquery)
    results = await db.execute(stmt)
    users = results.scalars().all()
    for user in users:
        if user.id != user_id:
            return user.id


async def get_thread_id(db: Session, id: int):
    result: Result = await db.execute(
        select(user_model.User).where(user_model.User.id == id)
    )
    user = result.scalar_one_or_none()
    thread_id = user.thread_id
    return thread_id
