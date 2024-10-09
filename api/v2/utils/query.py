from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

import v2.models.user as user_model


def get_user_by_raspi_id(db: Session, id: int):
    return db.query(user_model.User).filter(user_model.User.raspi_id == id).first()


async def get_user_id_same_couple(db: AsyncSession, user_id: int):
    # user_idからそのユーザのcouple_idを取得する
    result: Result = await db.execute(
        select(user_model.User).where(user_model.User.id == user_id)
    )
    user = result.scalar_one_or_none()
    couple_id = user.couple_id

    # そのcouple_idからもう片方のuser_idを取得する
    query = select(user_model.User).where(user_model.User.couple_id == couple_id)
    query = query.where(user_model.User.id != user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    boddy_id = user.id
    return boddy_id


async def get_thread_id(db: Session, id: int):
    result: Result = await db.execute(
        select(user_model.User).where(user_model.User.id == id)
    )
    user = result.scalar_one_or_none()
    thread_id = user.thread_id
    return thread_id
