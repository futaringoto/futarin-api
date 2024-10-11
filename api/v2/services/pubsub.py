from azure.messaging.webpubsubservice import WebPubSubServiceClient

from v2.utils.config import get_pubsub_connection_string

CONNECTION_STRING = get_pubsub_connection_string()


def get_service() -> WebPubSubServiceClient:
    service = WebPubSubServiceClient.from_connection_string(
        CONNECTION_STRING,
        hub="futarin_raspi",
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
