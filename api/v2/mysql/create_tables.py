from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from v2.utils.config import get_db_url, get_async_db_url

ASYNC_DB_URL = get_async_db_url()
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

DB_URL = get_db_url()
engine = create_engine(DB_URL, echo=True)

Base = declarative_base()

class Couple(Base):
    __tablename__ = "couples"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    users = relationship("User", back_populates="couple")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    couple_id = Column(Integer, ForeignKey("couples.id"))
    name = Column(String(20))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    couple = relationship("Couple", back_populates="couples")
    texts = relationship("Text", back_populates="user")
    messages = relationship("Message", back_populates="user")

class Text(Base):
    __tablename__ = "texts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    prompt = Column(String(1000))
    generated_text = Column(String(1000))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="texts")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    send_message = Column(String(1000))

    user = relationship("User", back_populates="messages")

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)