from openai import OpenAI
from v1.utils.config import (
    get_openai_api_key,
    get_openai_assistant_id,
    get_openai_thread_id,
)


OpenAI.api_key = get_openai_api_key()
ASSISTANT_ID = get_openai_assistant_id()
THREAD_ID = get_openai_thread_id()
client = OpenAI()


def generate_text(prompt: str) -> str:
    client.beta.threads.messages.create(
        thread_id=THREAD_ID,
        role="user",
        content=prompt,
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=THREAD_ID,
        assistant_id=ASSISTANT_ID,
    )

    messages = list(
        client.beta.threads.messages.list(thread_id=THREAD_ID, run_id=run.id)
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
