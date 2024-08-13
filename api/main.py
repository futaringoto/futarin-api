from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI

from v0.routers import raspi as v0_raspi
from v1.routers import raspi as v1_raspi
from v1.routers import sandbox as v1_sandbox
from v0.utils.config import check_env_variables as v0_check_env_variables
from v1.utils.config import check_env_variables as v1_check_env_variables


@asynccontextmanager
async def lifespan(app: FastAPI):
    v0_check_env_variables()
    v1_check_env_variables()
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)
app.include_router(v0_raspi.router)
app.include_router(v1_raspi.router, prefix="/v1/raspi")
app.include_router(v1_sandbox.router, prefix="/v1/sandbox")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
