import json
import os

import aiofiles
from fastapi import APIRouter, Header, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse

from v2.services.pubsub import get_service_demo

router = APIRouter()


@router.get("/get/logs", summary="ログの取得", response_class=HTMLResponse)
async def get_logs():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "../utils/index.html")

    async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
        html_content = await file.read()
    return html_content


@router.options("/demo/eventhandler")
async def handle_options(request: Request):
    # WebHook-Request-Origin ヘッダーをチェック
    if request.headers.get("WebHook-Request-Origin"):
        response = Response()
        response.headers["WebHook-Allowed-Origin"] = "*"
        return response

    return Response(status_code=400)  # ヘッダーがない場合は 400 (Bad Request) を返す


@router.post("/demo/eventhandler")
async def handle_event(
    request: Request, ce_userid: str = Header(None), ce_type: str = Header(None)
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
        return Response(content=f"{ce_userid} connected", status_code=200)

    elif ce_type == "azure.webpubsub.user.message":
        body = await request.body()
        message = body.decode("UTF-8")
        service = get_service_demo()

        # Assuming `service.send_to_all` is defined somewhere in your code
        service.send_to_all(
            content_type="application/json",
            message={"from": ce_userid, "message": message},
        )

        return Response(status_code=204, media_type="text/plain")

    else:
        return Response(content="Bad Request", status_code=400)


@router.post("/demo/negotiate/{id}", summary="websocketsのURL発行")
async def negotiate(id: int):
    if not id:
        return "missing user id", 400
    service = get_service_demo()
    token = service.get_client_access_token(user_id=id)
    return {"url": token["url"]}
