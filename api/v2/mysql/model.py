import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp

from db import Base


class User(Base):
    __tablename__ ="users"

    id = Column(String, primary_key=True)
    username = Column(String)


class Text(Base):
    __tablename__ = "texts"

    id = Column(String, primary_key=True)
    uuid = Column(String, ForeignKey("users.id"))
    prompt = Column(String(1024))
    generated_text = Column(String(1024))
    created_at = Column(DateTime, server_default=current_timestamp())


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True)
    uuid = Column(String, ForeignKey("users.id"))
    message = Column(String(1024))


class Group(Base):
    __tablename__ = "groups"

    id = Column(String, primary_key=True)
    uuid1 = Column(String, ForeignKey("users.id"))
    uuid2 = Column(String, ForeignKey("users.id"))

    