import os

from azure.storage.blob import BlobServiceClient
from sqlalchemy.ext.asyncio import AsyncSession

import v2.models.message as message_model
from v2.utils.config import get_azure_sas_token, get_azure_storage_account

DOWNLOAD_DIR = "downloads"


def get_blob_storage_account():
    azure_storage_account = get_azure_storage_account()
    account_url = f"https://{azure_storage_account}.blob.core.windows.net"
    sas_token = get_azure_sas_token()
    blob_service_client = BlobServiceClient(account_url, credential=sas_token)
    return blob_service_client


def has_blob_file(id: int, blob_service_client: BlobServiceClient):
    container_name = "message"
    container_client = blob_service_client.get_container_client(
        container=container_name
    )

    blob_list = []
    for blob in container_client.list_blobs():
        blob_list.append(int(blob.name))

    if id in blob_list:
        return True
    else:
        return False


async def upload_blob_file(
    user_id: int, blob_service_client: BlobServiceClient, db: AsyncSession, data
):
    container_name = "message"
    # コンテナクライアントの取得
    container_client = blob_service_client.get_container_client(
        container=container_name
    )
    blob_name = str(user_id)
    # Blobクライアントの作成
    blob_client = container_client.get_blob_client(blob_name)
    # Blobをアップロード
    blob_client.upload_blob(data=data, overwrite=True)

    # messageテーブルにUpdate
    blob_url = blob_client.url
    message = message_model.Message(user_id=user_id, file_url=blob_url)
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return {"id": user_id, "message": blob_url}


def download_blob_file(
    user_id: int, boddy_id: int, blob_service_client: BlobServiceClient
):
    container_name = "message"
    container_client = blob_service_client.get_container_client(
        container=container_name
    )

    for blob in container_client.list_blobs():
        if boddy_id == int(blob.name):
            download_file_path = os.path.join(DOWNLOAD_DIR, f"{boddy_id}.wav")
            with open(file=download_file_path, mode="wb") as download_file:
                download_file.write(container_client.download_blob(blob.name).readall())
            return {"id": user_id, "message": "ダウンロードが完了しました"}

    return {"id": user_id, "message": "相方のファイルは見つかりませんでした"}
