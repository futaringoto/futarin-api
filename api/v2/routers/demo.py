import os
import aiofiles
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get(
    "/get/logs",
    summary="ログの取得",
    # response_class=HTMLResponse
)
async def get_logs():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "../utils/index.html")

    async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
        html_content = await file.read()
    return html_content
