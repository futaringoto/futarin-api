import json
import asyncio
import aiohttp
import websockets

# /negotiate エンドポイントのURL
negotiate_url = "https://darling-readily-collie.ngrok-free.app/demo/negotiate/1"

# WebSocket接続URLを取得する関数
async def get_connection_url():
    async with aiohttp.ClientSession() as session:
        async with session.post(negotiate_url) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("url")  # ネゴシエーションで取得したURLを返す
            else:
                print(f"Failed to negotiate: {response.status}")
                return None


# WebSocket通信を行う関数
async def hello():
    connection_url = await get_connection_url()

    if not connection_url:
        print("Could not retrieve WebSocket connection URL")
        return

    # WebSocketに接続
    async with websockets.connect(connection_url) as ws:
        print("Connected to Web PubSub!")

        # メッセージの送信
        await ws.send("Hello, Server!")

        # 無限ループでメッセージ受信を待つ
        while True:
            try:
                message = await ws.recv()
                data = json.loads(message)
                print(data)
                # for i, text in enumerate(data.values()):
                #     if i == 2:
                #         decoded_message = text.decode("utf-8")
                #         print(f"Received message: {decoded_message}")
            except websockets.exceptions.ConnectionClosedOK:
                print("Connection closed by the server")
                break

if __name__ == "__main__":
    asyncio.run(hello())