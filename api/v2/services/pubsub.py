from azure.messaging.webpubsubservice import WebPubSubServiceClient

from v2.utils.config import get_pubsub_connection_string

CONNECTION_STRING = get_pubsub_connection_string()


def get_service() -> WebPubSubServiceClient:
    service = WebPubSubServiceClient.from_connection_string(
        CONNECTION_STRING,
        hub="futarin_raspi",
    )
    return service


def push_id_to_raspi_id(raspi_id: int, user_id: int):
    service = get_service()
    res = service.send_to_user(
        user_id=str(raspi_id),
        message={
            "type": "message",
            "id": str(user_id)
        }
    )
    return res
