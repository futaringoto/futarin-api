from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import logging
import json
import time

connect_str = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqFwYtK6RU2tCw8J6h9hHQmhZLZ2AZdTF3aa52RSbIQoe1xtlY+cwlSogz3UfnKOMIoTjeQ==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "futarin-log"

container_client = blob_service_client.get_container_client(container_name)

def upload_json_to_blob(json_data):
    try:
        logging.info(f"Generated log: {json_data}")
        blob_name = f"log_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        json_str = json.dumps(json_data)
        blob_client = container_client.get_blob_client(blob_name)

        # Blobにログデータを書き込む
        blob_client.upload_blob(json_str, overwrite=True)
        logging.info(f"Uploaded JSON to {blob_name}")
    except Exception as ex:
        logging.error(f"Error uploading JSON to Blob Storage: {ex}")
