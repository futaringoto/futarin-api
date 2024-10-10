from openai import OpenAI

from v1.utils.config import get_openai_assistant_id
from v2.utils.config import get_openai_api_key

OpenAI.api_key = get_openai_api_key()
client = OpenAI()

ASSISTANT_ID = get_openai_assistant_id()


def generate_text(thread_id: int, prompt: str) -> str:
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt,
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
    )

    messages = list(
        client.beta.threads.messages.list(thread_id=thread_id, run_id=run.id)
    )
    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []

    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(
            annotation.text, f"[{index}]"
        )

        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")

    return message_content.value
