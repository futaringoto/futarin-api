from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine.url import URL

from v2.utils.config import get_is_dev_mode, get_db_object

IS_DEV_MODE: bool = get_is_dev_mode()
DB_OBJECT: Dict[str, str] = get_db_object()

url_dev = URL.create(
    drivername="mysql+aiomysql",
    username="root",
    password="password",
    host="mysql",
    database="futaringoto_db",
    query={"charset": "utf8"},
)

url_prod = URL.create(
    drivername="mysql+aiomysql",
    username=DB_OBJECT["username"],
    password=DB_OBJECT["password"],
    host=DB_OBJECT["host"],
    database=DB_OBJECT["database"],
    query={"charset": "utf8"},
)

url = url_dev if IS_DEV_MODE else url_prod

async_engine = create_async_engine(url, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base = declarative_base()
