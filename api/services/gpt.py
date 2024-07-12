from openai import OpenAI
from utils.config import get_openai_api_key

OpenAI.api_key = get_openai_api_key()
client = OpenAI()

def generate_text(input_text: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "テスト期間中の学生を親の視点から励ますような言葉を生成してください。"},
            {"role": "user", "content": input_text}
        ]
    )
    return completion.choices[0].message.content
