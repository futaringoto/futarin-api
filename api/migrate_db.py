from sqlalchemy import create_engine
from azure.storage.blob import BlobServiceClient

from db import Base
from v2.models import Couple, Message, User  # noqa: F401
from v2.utils.config import get_db_url, get_azure_sas_token, get_azure_storage_account

DB_URL = get_db_url()
engine = create_engine(DB_URL, echo=True)

#azureの認証
azure_storage_account = get_azure_storage_account()
account_url = f"https://{azure_storage_account}.blob.core.windows.net"
sas_token = get_azure_sas_token()
blob_service_client = BlobServiceClient(account_url, credential=sas_token)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def create_azure_container():
    container_name = "message"
    blob_service_client.create_container(container_name)


if __name__ == "__main__":
    reset_database()
    create_azure_container()
