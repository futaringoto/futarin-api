from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import v2.models.couple as couple_model
import v2.models.user as user_model
import v2.schemas.couple as couple_schema
from v2.utils.logging import get_logger

logger = get_logger()


def validate_users(user1, user2) -> bool:
    # ユーザーが存在するか確認
    if not user1 or not user2:
        return False
    # すでにどちらかのユーザーがカップルに属しているか確認
    if user1.couple_id is not None or user2.couple_id is not None:
        return False
    return True


async def create_couple(
    db: AsyncSession, couple_create: couple_schema.CoupleCreate
) -> couple_model.Couple:
    couple = couple_model.Couple(name=couple_create.name)
    db.add(couple)
    await db.flush()
    stmt = select(user_model.User).where(
        user_model.User.id.in_([couple_create.user1_id, couple_create.user2_id])
    )
    result = await db.execute(stmt)
    users = result.scalars().all()

    if not validate_users(users[0], users[1]):
        raise ValueError("不正なuser_idです。")

    for user in users:
        user.couple_id = couple.id

    # 変更をコミット
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


async def get_user_id_same_couple(
    db: AsyncSession, user_id: int
):
    #user_idからそのユーザのcouple_idを取得する
    result: Result = await db.execute(
        select(user_model.User).where(user_model.User.id == user_id)
    )
    user = result.scalar_one_or_none()
    couple_id = user.couple_id

    #そのcouple_idからもう片方のuser_idを取得する
    query = select(user_model.User).where(user_model.User.couple_id == couple_id)
    query = query.where(user_model.User.id != user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    boddy_id = user.id
    return boddy_id
