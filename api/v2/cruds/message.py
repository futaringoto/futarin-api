from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import v2.models.message as messsage_model


class ForeignKeyError(Exception):
    pass


async def create_message(
    db: AsyncSession,
    user_id: int,
    content: str,
):
    try:
        message = messsage_model.Message(user_id=user_id, content=content)
        db.add(message)
        await db.commit()
        await db.refresh(message)
    except IntegrityError as e:
        if "foreign key" in str(e.orig):
            raise ForeignKeyError("Related resource not found")
        raise


async def get_histories(
    db: AsyncSession,
    user_id: int,
):
    result: Result = await db.execute(
        select(messsage_model.Message).filter(messsage_model.Message.user_id == user_id)
    )
    messages = result.all()
    return [message[0].content for message in messages] if messages else []
