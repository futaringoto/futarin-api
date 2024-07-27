from azure.storage.blob import BlobServiceClient
from utils.config import get_storage_account_name, get_sas_token, is_dev_mode
import logging
import json
import time

STORAGE_ACCOUNT_NAME = get_storage_account_name()
SAS_TOKEN = get_sas_token()

def upload_json_to_blob(json_data):
    if is_dev_mode: return 0
    account_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(account_url, credential=SAS_TOKEN)
    container_name = "futarin-log"
    container_client = blob_service_client.get_container_client(container_name)

    try:
        logging.info(f"Generated log: {json_data}")
        blob_name = f"log_{time.strftime('%Y%m%d_%H%M%S')}.json"
        json_str = json.dumps(json_data, ensure_ascii=False)
        blob_client = container_client.get_blob_client(blob_name)

        # Blobにログデータを書き込む
        blob_client.upload_blob(json_str, overwrite=True)
        logging.info(f"Uploaded JSON to {blob_name}")
    except Exception as ex:
        logging.error(f"Error uploading JSON to Blob Storage: {ex}")
