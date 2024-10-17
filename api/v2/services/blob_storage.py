import os

from azure.storage.blob import BlobServiceClient

from config import get_azure_sas_token, get_azure_storage_account

DOWNLOAD_DIR = "downloads"
AZURE_STORAGE_ACCOUNT = get_azure_storage_account()


def get_blob_service_client():
    account_url = f"https://{AZURE_STORAGE_ACCOUNT}.blob.core.windows.net"
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


async def upload_blob_file(user_id: int, blob_service_client: BlobServiceClient, data):
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

    return {"id": user_id, "message": "メッセージをアップロードしました"}


def is_downloaded_blob(boddy_id: str, blob_service_client: BlobServiceClient):
    container_name = "message"
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=str(boddy_id)
    )
    download_file_path = os.path.join(DOWNLOAD_DIR, f"{boddy_id}.wav")

    if not blob_client.exists():
        return False

    with open(file=download_file_path, mode="wb") as download_file:
        download_data = blob_client.download_blob()
        download_file.write(download_data.readall())

    blob_client.delete_blob()
    return True
