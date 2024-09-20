from pydantic import BaseModel, Field


class TextResponse(BaseModel):
    text: str = Field(None, json_schema_extra={"example": "文字列だけ返します。"})
