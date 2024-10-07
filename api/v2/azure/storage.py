from azure.storage.blob import BlobServiceClient
from sqlalchemy.ext.asyncio import AsyncSession

import v2.models.message as message_model
from v2.utils.config import get_azure_storage_account, get_azure_sas_token


def get_blob_storage_account():
    azure_storage_account = get_azure_storage_account()
    account_url = f"https://{azure_storage_account}.blob.core.windows.net"
    sas_token = get_azure_sas_token()
    blob_service_client = BlobServiceClient(account_url, credential=sas_token)
    return blob_service_client


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
    message = message_model.Message(user_id=user_id, file_url=blob_url)
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return {"id": user_id, "message": blob_url}


async def download_blob_file(
    user_id: int, blob_service_client: BlobServiceClient
):
    container_name = "message"
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=str(user_id))
    blob_url = blob_client.url
    return blob_url