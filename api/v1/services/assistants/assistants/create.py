from openai import OpenAI

from v1.utils.config import get_openai_api_key

OpenAI.api_key = get_openai_api_key()
client = OpenAI()


def create_assistant() -> str:
    assistant = client.beta.assistants.create(
        name="futarin",
        instructions="あなたは、プロのカウンセラーです。\
            与えられたファイルをもとに相談者の気持ちに寄り添い、解決策を提示しながら、簡潔でフレンドリーなひとまとまりのメッセージを生成してください。\
            日本語で50文字程度でお願いします。\
        ",
        model="gpt-4o-mini",
        tools=[{"type": "file_search"}],
    )
    return assistant
