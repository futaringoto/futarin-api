import asyncio
import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import HTTPStatusError, RequestError

from v2.services.gpt import generate_text
from db import get_db
from v2.utils.query import get_user_by_raspi_id
from v2.rag.vector_db import generate_question


router = APIRouter()

@router.post(
    "/conversation",
    tags=["futarin-RAG"],
    summary="ふたりんとの会話",
)
async def conversation(
    raspi_id: int,
    prompt: str,
    speaker: int = 1,
    mode: int = 0,
    db: AsyncSession = Depends(get_db)
):
    # 返答の生成
    try:
        get_user_task = asyncio.create_task(get_user_by_raspi_id(db, raspi_id))
        user = await get_user_task
        thread_id = user.thread_id
        response: str = await generate_text(mode, thread_id, prompt)
    except (RequestError, HTTPStatusError) as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    # プロンプトの保存
    with open(f"/api/v2/rag/text/{raspi_id}_prompt.txt", "a") as f:
        f.write(f"{prompt}\n")

    return response


@router.post(
    "/questions",
    tags=["futarin-RAG"],
    summary="質問の生成",
)
async def get_questions(
    raspi_id: int
):
    result = generate_question(raspi_id)
    return result
