from azure.messaging.webpubsubservice import WebPubSubServiceClient
from sqlalchemy.ext.asyncio import AsyncSession

import v2.cruds.raspi as raspi_crud
from config import get_pubsub_connection_string
from v2.utils.logging import get_logger

CONNECTION_STRING = get_pubsub_connection_string()
logger = get_logger()


def get_service() -> WebPubSubServiceClient:
    service = WebPubSubServiceClient.from_connection_string(
        CONNECTION_STRING,
        hub="futarin_raspi",
    )
    return service


def get_service_demo() -> WebPubSubServiceClient:
    service = WebPubSubServiceClient.from_connection_string(
        CONNECTION_STRING,
        hub="demo",
    )
    return service


async def push_id_to_raspi_id(
    service: WebPubSubServiceClient, receiver_raspi_id: int, sender_user_id: int
):
    res = service.send_to_user(
        user_id=str(receiver_raspi_id),
        message={"type": "message", "id": str(sender_user_id)},
    )
    return res


async def push_transcription(
    db: AsyncSession, service: WebPubSubServiceClient, raspi_id: int, transcription: str
):
    raspi_name = await raspi_crud.get_raspi_name(db, raspi_id)
    res = service.send_to_all(
        {
            "type": "transcription",
            "raspi_name": raspi_name,
            "text": transcription,
        }
    )
    logger.info(f"res: {res}")
    return res


def push_text(service: WebPubSubServiceClient, raspi_id: int, generated_text: str):
    res = service.send_to_all(
        {
            "type": "generated_text",
            "raspi_id": str(raspi_id),
            "text": generated_text,
        }
    )
    logger.info(f"res: {res}")
    return res


def get_negotiation_url(service: WebPubSubServiceClient):
    token = service.get_client_access_token()
    return token["url"]
