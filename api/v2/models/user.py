from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    couple_id = Column(
        Integer, ForeignKey("couples.id", ondelete="SET NULL"), nullable=True
    )
    name = Column(String(20), nullable=False)
    thread_id = Column(String(45), nullable=False)
    raspi_id = Column(Integer, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    couple = relationship("Couple", back_populates="users")
    messages = relationship("Message", back_populates="user")
