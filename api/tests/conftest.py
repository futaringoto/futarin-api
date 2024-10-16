from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from db import Base, get_db
from main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    # Async用のengineとsessionを作成
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )

    # テスト用にオンメモリのSQLiteテーブルを初期化（関数ごとにリセット）
    async with async_engine.begin() as conn:
        await conn.execute(text("PRAGMA foreign_keys = ON"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    async def get_test_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    # クリーンアップ処理があればここに記述（必要に応じて）
    await async_engine.dispose()
