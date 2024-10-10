from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db import Base


class Raspi(Base):
    __tablename__ = "raspis"

    id = Column(Integer, primary_key=True)
    connection_id = Column(String(50), nullable=True)
    name = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="raspi")
