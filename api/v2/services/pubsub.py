from azure.messaging.webpubsubservice import WebPubSubServiceClient

from v2.utils.config import get_pubsub_connection_string

CONNECTION_STRING = get_pubsub_connection_string()


def get_service() -> WebPubSubServiceClient:
    service = WebPubSubServiceClient.from_connection_string(
        CONNECTION_STRING,
        hub="futarin_raspi",
    )
    return service


def push_id(id: int):
    service = get_service()
    res = service.send_to_all({"user_id": str(id)})
    return res
