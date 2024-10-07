from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from azure.storage.blob import BlobServiceClient

from db import Base
from v2.models import Couple, Message, User  # noqa: F401
from v2.utils.config import get_azure_sas_token, get_azure_storage_account

DB_URL = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="password",
    host="mysql",
    database="futaringoto_db",
    query={"charset": "utf8"},
)

engine = create_engine(DB_URL, echo=True)

#azureの認証
azure_storage_account = get_azure_storage_account()
account_url = f"https://{azure_storage_account}.blob.core.windows.net"
sas_token = get_azure_sas_token()
blob_service_client = BlobServiceClient(account_url, credential=sas_token)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
