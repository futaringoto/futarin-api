from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db import Base


class Couple(Base):
    __tablename__ = "couples"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    users = relationship("User", back_populates="couple")
