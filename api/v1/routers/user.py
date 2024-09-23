from fastapi import APIRouter

router = APIRouter()


@router.post("/add_users", tags=["users"], summary="mysqlにuserを登録")
async def add_user():
    return {"message": "user"}
