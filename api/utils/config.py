import os

def get_voicevox_url():
    return os.getenv("VOICEVOX_URL")

def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")
