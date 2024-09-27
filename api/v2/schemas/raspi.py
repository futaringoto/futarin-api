from pydantic import BaseModel, ConfigDict, Field


class RaspiBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RaspiMessageResponse(RaspiBase):
    id: int
    message: str = Field(None, json_schema_extra={"example": "successed!"})
