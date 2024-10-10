from fastapi import APIRouter, Request

from v2.utils.logging import get_logger

router = APIRouter()
logger = get_logger()


@router.post(
    "/eventhandler",
    tags=["WebSockets"],
    summary="イベント処理",
)
async def handle_event(request: Request):
    event = await request.json()

    if event["event"] == "connected":
        connection_id = event["connectionId"]
        print(f"Client connected: {connection_id}")

    elif event["event"] == "disconnected":
        connection_id = event["connectionId"]
        print(f"Client disconnected: {connection_id}")

    return {"status": "ok"}
