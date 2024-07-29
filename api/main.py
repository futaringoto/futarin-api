from typing import Union
from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
from routers import raspi

def check_env_variables():
    env_vars = [
        "OPENAI_API_KEY",
        "VOICEVOX_API_KEY",
        "STORAGE_ACCOUNT_NAME",
        "SAS_TOKEN",
    ]
    missing_vars = [var for var in env_vars if os.getenv(var) is None]
    if missing_vars:
        raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    check_env_variables()
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)
app.include_router(raspi.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
