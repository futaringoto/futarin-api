from sqlalchemy import create_engine

from db import Base
from v2.models import Couple, Message, User  # noqa: F401
from v2.utils.config import get_db_url

DB_URL = get_db_url()

engine = create_engine(DB_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
