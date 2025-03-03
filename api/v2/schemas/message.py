from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    user_id: int = Field(...)
    content: str = Field(...)


class MessageCreate(MessageBase):
    pass
