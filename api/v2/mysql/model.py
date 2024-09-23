from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from db import Base

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

    id = Column(String, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    prompt = Column(String(1000))
    generated_text = Column(String(1000))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="texts")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    send_message = Column(String(1000))

    user = relationship("User", back_populates="messages")
