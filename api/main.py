from contextlib import asynccontextmanager
from datetime import datetime
from typing import Union

from fastapi import FastAPI

from v0.routers import raspi as v0_raspi
from v0.utils.config import check_env_variables as v0_check_env_variables
from v1.routers import raspi as v1_raspi
from v1.routers import sandbox as v1_sandbox
from v1.utils.config import check_env_variables as v1_check_env_variables
from v2.routers import couple as v2_couple
from v2.routers import demo as v2_demo
from v2.routers import pubsub as v2_pubsub
from v2.routers import raspi as v2_raspi
from v2.routers import user as v2_user
from v2.services.pubsub import push_id_to_raspi_id
from v2.utils.config import check_env_variables as v2_check_env_variables


@asynccontextmanager
async def lifespan(app: FastAPI):
    v0_check_env_variables()
    v1_check_env_variables()
    v2_check_env_variables()
    yield
    print("Shutting down...")


tags_metadata = [
    {
        "name": "futarin-raspi",
        "description": "[futairn-raspi]()から使用するエンドポイント",
    },
    {
        "name": "sandbox",
        "description": "デバッグ用",
    },
    {
        "name": "raspis",
    },
    {
        "name": "users",
    },
    {
        "name": "couples",
    },
    {
        "name": "v1",
        "description": "**Deprecated (非推奨)**",
    },
    {
        "name": "v0 (deprecated)",
        "description": "**Deprecated (非推奨)** URI変更なし",
    },
]

app = FastAPI(
    lifespan=lifespan,
    openapi_tags=tags_metadata,
    title="futarin-api",
    description="詳しくは[github](https://github.com/futaringoto/futarin-api)",
    summary="「ふたりんごと」のAPI",
    version="v1",
    contact={
        "name": "futaringoto",
        "url": "https://github.com/futaringoto",
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/futaringoto/futarin-api/blob/main/LICENSE",
    },
)
app.include_router(v0_raspi.router)
app.include_router(v1_raspi.router, prefix="/v1/raspi")
app.include_router(v1_sandbox.router, prefix="/v1/sandbox")
app.include_router(v2_raspi.router, prefix="/v2/raspis")
app.include_router(v2_user.router, prefix="/v2/users")
app.include_router(v2_couple.router, prefix="/v2/couples")
app.include_router(v2_pubsub.router, prefix="/v2")
app.include_router(v2_demo.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/push/{raspi_id}/messages/{user_id}")
def push(raspi_id, user_id):
    return push_id_to_raspi_id(raspi_id, user_id)


@app.get("/ping")
def ping():
    return {"message": "pong", "timestamp": datetime.now()}
