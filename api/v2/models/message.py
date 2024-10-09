from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="messages")
