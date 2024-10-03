from azure.storage.blob import BlobServiceClient


def upload_blob_file(blob_service_client: BlobServiceClient, container_name: str, data):
    container_client = blob_service_client.get_container_client(container=container_name)
    name = f"{container_name}'s file"
    container_client.upload_blob(name=name, data=data, overwrite=True)
