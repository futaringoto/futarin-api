from openai import AsyncOpenAI

from config import get_openai_api_key, get_openai_assistant_id, get_openai_assistant_id_paraphrase

AsyncOpenAI.api_key = get_openai_api_key()
client = AsyncOpenAI()

ASSISTANT_ID = get_openai_assistant_id()
ASSISTANT_ID_PARAPHRASE = get_openai_assistant_id_paraphrase()


async def create_new_thread_id() -> str:
    thread = await client.beta.threads.create()
    return thread.id


async def delete_thread_id(thread_id: str):
    await client.beta.threads.delete(thread_id)


async def generate_text(mode: int, thread_id: int, prompt: str) -> str:
    mode_dispatch = {
        0: generate_text_normal,
        1: generate_text_change,
    }

    try:
        handler = mode_dispatch[mode]
        return await handler(thread_id, prompt)

    except KeyError:
        raise ValueError(f"Invalid mode: {mode}.")


async def generate_text_normal(thread_id: int, prompt: str) -> str:
    await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt,
    )

    run = await client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
    )

    messages = await client.beta.threads.messages.list(
        thread_id=thread_id, run_id=run.id
    )
    message_content = messages.data[0].content[0].text
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


async def generate_text_change(thread_id: int, prompt: str) -> str:
    await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt,
    )

    run = await client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID_PARAPHRASE,
    )

    messages = await client.beta.threads.messages.list(
        thread_id=thread_id, run_id=run.id
    )
    message_content = messages.data[0].content[0].text
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
