from openai import OpenAI
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import v2.models.user as user_model
import v2.schemas.user as user_schema
from v2.utils.config import get_openai_api_key

client = OpenAI(
    api_key=get_openai_api_key()
)


async def create_user(
    db: AsyncSession, user_create: user_schema.UserCreate
) -> user_model.User:
    # 引数にスキーマuser_create: user_schema.UserCreateを受け取りDBモデルのuser_model.Userに変換する
    user = user_model.User(**user_create.dict())
    thread = client.beta.threads.create()
    user.thread_id = thread.id

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_users(db: AsyncSession):
    result: Result = await db.execute(
        select(
            user_model.User.id,
            user_model.User.couple_id,
            user_model.User.name,
            user_model.User.thread_id,
            user_model.User.raspi_id,
            user_model.User.created_at,
            user_model.User.updated_at,
        )
    )
    return result.all()


async def get_user(db: AsyncSession, user_id: int):
    result: Result = await db.execute(
        select(user_model.User).filter(user_model.User.id == user_id)
    )
    user = result.first()
    return user[0] if user is not None else None


async def update_user(
    db: AsyncSession, user_update: user_schema.UserUpdate, original: user_model.User
) -> user_model.User:
    original.couple_id = user_update.couple_id
    original.name = user_update.name
    original.raspi_id = user_update.raspi_id
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_user(db: AsyncSession, original: user_model.User) -> None:
    await db.delete(original)
    await db.commit()
