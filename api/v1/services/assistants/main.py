from openai import OpenAI

from v1.utils.config import get_openai_api_key

OpenAI.api_key = get_openai_api_key
client = OpenAI()


def create_thread():
    response = client.beta.threads.create()
    return response


def create_run(assistant_id: str, input_data: dict):
    response = openai.Assistant.create_run(assistant_id=assistant_id, input=input_data)
    return response
