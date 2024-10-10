from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

import v2.models.user as user_model


def get_user_by_raspi_id(db: Session, id: int):
    return db.query(user_model.User).filter(user_model.User.raspi_id == id).first()


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
