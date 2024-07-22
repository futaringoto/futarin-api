import os

def get_voicevox_url():
    return os.getenv("VOICEVOX_URL")

def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")

def get_storage_account_name():
    return os.getenv("STORAGE_ACCOUNT_NAME")

def get_sas_token():
    return os.getenv("SAS_TOKEN")
