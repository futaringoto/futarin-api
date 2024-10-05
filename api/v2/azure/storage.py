from azure.storage.blob import BlobServiceClient
from sqlalchemy.ext.asyncio import AsyncSession

import v2.models.message as message_model


async def upload_blob_file(
    user_id: int, blob_service_client: BlobServiceClient, db: AsyncSession, data
):
    container_name = "message"
    #コンテナクライアントの取得
    container_client = blob_service_client.get_container_client(container=container_name)
    blob_name = str(user_id)
    #Blobクライアントの作成
    blob_client = container_client.get_blob_client(blob_name)
    #Blobをアップロード
    blob_client.upload_blob(data=data, overwrite=True)

    #messageテーブルにUpdate
    blob_url = blob_client.url
    message = message_model.Message(user_id=user_id, azure_url=blob_url)
    db.add(message)
    await db.commit()
    await db.refresh(message)