from openai import OpenAI

from v0.utils.config import get_openai_api_key

OpenAI.api_key = get_openai_api_key()
client = OpenAI()


def generate_text(input_text: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "テスト期間中の学生を親の視点から励ますような言葉を生成してください。日本語で40文字程度になるようにお願いします。",
            },
            {"role": "user", "content": input_text},
        ],
    )
    return completion.choices[0].message.content
