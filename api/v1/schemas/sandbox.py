from pydantic import BaseModel, Field


class TextResponse(BaseModel):
    text: str = Field(None, example="文字列だけ返します。")
