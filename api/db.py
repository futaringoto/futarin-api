import ssl
from typing import Dict

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from v2.utils.config import get_db_object, get_is_dev_mode, get_ssl_cert_path

IS_DEV_MODE: bool = get_is_dev_mode()


def create_dev_async_engine():
    url = URL.create(
        drivername="mysql+aiomysql",
        username="root",
        password="password",
        host="mysql",
        database="futaringoto_db",
        query={"charset": "utf8"},
    )
    async_engine = create_async_engine(url, echo=True)
    return async_engine


def create_prod_async_engine():
    DB_OBJECT: Dict[str, str] = get_db_object()
    SSL_CERT_PATH = get_ssl_cert_path()
    ssl_context = ssl.create_default_context(cafile=SSL_CERT_PATH)
    url = URL.create(
        drivername="mysql+aiomysql",
        username=DB_OBJECT["username"],
        password=DB_OBJECT["password"],
        host=DB_OBJECT["host"],
        database=DB_OBJECT["database"],
        query={"charset": "utf8"},
    )
    async_engine = create_async_engine(
        url, connect_args={"ssl": ssl_context}, echo=True
    )
    return async_engine


async_engine = create_dev_async_engine() if IS_DEV_MODE else create_prod_async_engine()
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)


# Base = declarative_base()
class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session
