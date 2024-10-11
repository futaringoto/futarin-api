import json

from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from v2.cruds.raspi import get_raspi, update_ws_active
from v2.services.pubsub import get_service
from v2.utils.logging import get_logger

router = APIRouter()
logger = get_logger()


@router.options("/eventhandler")
async def handle_options(request: Request):
    # WebHook-Request-Origin ヘッダーをチェック
    if request.headers.get("WebHook-Request-Origin"):
        response = Response()
        response.headers["WebHook-Allowed-Origin"] = "*"
        return response

    return Response(status_code=400)  # ヘッダーがない場合は 400 (Bad Request) を返す


@router.post("/eventhandler")
async def handle_event(
    request: Request,
    ce_userid: str = Header(None),
    ce_type: str = Header(None),
    db: AsyncSession = Depends(get_db),
):
    print("Received event of type:", ce_type)

    if ce_type == "azure.webpubsub.sys.connect":
        body = await request.body()
        body_str = body.decode("utf-8")
        print("Reading from connect request body...")

        try:
            query = json.loads(body_str)["query"]
            print("Reading from request body query:", query)
        except KeyError:
            raise HTTPException(
                status_code=400, detail="Missing 'query' in request body"
            )

        id_element = query.get("id")
        user_id = id_element[0] if id_element else None

        if user_id:
            return JSONResponse(content={"userId": user_id}, status_code=200)
        else:
            return JSONResponse(content="missing user id", status_code=401)

    elif ce_type == "azure.webpubsub.sys.connected":
        # raspi = await get_raspi(db, raspi_id=int(ce_userid))
        # await update_ws_active(True, db, raspi)
        return Response(content=f"{ce_userid} connected", status_code=200)

    elif ce_type == "azure.webpubsub.user.message":
        body = await request.body()
        message = body.decode("UTF-8")
        service = get_service()

        # Assuming `service.send_to_all` is defined somewhere in your code
        service.send_to_all(
            content_type="application/json",
            message={"from": ce_userid, "message": message},
        )

        return Response(status_code=204, media_type="text/plain")

    elif ce_type == "azure.webpubsub.sys.disconnected":
        raspi = await get_raspi(db, raspi_id=int(ce_userid))
        await update_ws_active(False, db, raspi)
        return Response(content=f"{ce_userid} disconnected", status_code=200)

    else:
        return Response(content="Bad Request", status_code=400)
