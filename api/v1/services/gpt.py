import os
from openai import OpenAI
from v1.utils.config import get_openai_api_key
# from v1.services.db import insert_data

OpenAI.api_key = get_openai_api_key()
client = OpenAI()

def generate_text(prompt: str) -> str:
    assistant = client.beta.assistants.create(
        name="futarin",
        instructions=
            "あなたは、プロのカウンセラーです。与えられたファイルをもとに相談者の気持ちに寄り添い、解決策を提示しながら、簡潔でフレンドリーなメッセージを生成してください。",
        model="gpt-4o-mini",
        tools=[{"type": "file_search"}],
    )
     
    vs_name = "professional counselor"
    vector_store = client.beta.vector_stores.create(name=vs_name)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '../assets/file_search.txt')

    file_streams = [open(file_path, 'rb')]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search":{"vector_store_ids":[vector_store.id]}},
    )

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt,
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []

    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(annotation.text, f"[{index}]")

        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")

    message = message_content.value.replace("\n", "")
    # insert_data(prompt, message)
    return message