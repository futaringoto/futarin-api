import asyncio

from fastapi import APIRouter, Depends, HTTPException
from httpx import HTTPStatusError, RequestError
from sqlalchemy.ext.asyncio import AsyncSession

import v2.cruds.message as message_crud
from db import get_db
from v2.rag.vector_db import generate_question
from v2.services.gpt import generate_text
from v2.utils.query import get_user_by_raspi_id

router = APIRouter()


@router.post(
    "/conversation",
    tags=["futarin-RAG"],
    summary="ふたりんとの会話",
)
async def conversation(
    user_id: int,
    raspi_id: int,
    prompt: str,
    speaker: int = 1,
    mode: int = 0,
    db: AsyncSession = Depends(get_db),
) -> str:
    # 返答の生成
    try:
        get_user_task = asyncio.create_task(get_user_by_raspi_id(db, raspi_id))
        user = await get_user_task
        thread_id = user.thread_id
        response: str = await generate_text(mode, thread_id, prompt)

        # プロンプトの保存
        await message_crud.create_message(db, user_id, prompt)

    except (RequestError, HTTPStatusError) as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    return response


@router.post(
    "/questions",
    tags=["futarin-RAG"],
    summary="質問の生成",
)
async def get_questions(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await generate_question(db, user_id)
    return result.content


@router.get("/get_histories", tags=["futarin-RAG"], summary="履歴の取得")
async def get_histories(user_id: int, db: AsyncSession = Depends(get_db)):
    return await message_crud.get_histories(db, user_id)
