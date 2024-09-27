from pydantic import BaseModel, ConfigDict

class Raspi(BaseModel):
    model_config = ConfigDict(extra="forbid")
    user_id: int
