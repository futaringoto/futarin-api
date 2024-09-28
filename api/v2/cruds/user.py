from sqlalchemy.ext.asyncio import AsyncSession

import v2.models.user as user_model
import v2.schemas.user as user_schema


async def create_user(
    db: AsyncSession, user_create: user_schema.UserCreate
) -> user_model.User:
    # 引数にスキーマuser_create: user_schema.UserCreateを受け取りDBモデルのuser_model.Userに変換する
    user = user_model.User(**user_create.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
