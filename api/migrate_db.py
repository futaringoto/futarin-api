from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from db import Base
from v2.models import Couple, Message, Raspi, User  # noqa: F401

DB_URL = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="password",
    host="mysql",
    database="futaringoto_db",
    query={"charset": "utf8"},
)

engine = create_engine(DB_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
