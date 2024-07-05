from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.post(
    "/audio_query",
    tags=["voicevox クエリ作成"],
    summary="音声合成用のクエリを作成する"
)
def audio_query(
    text: str,
    speaker: int = 1,
    ):

    return FileResponse(

    )
