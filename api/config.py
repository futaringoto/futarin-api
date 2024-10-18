import os
from typing import Dict


def check_env_variables():
    is_dev_mode: bool = get_is_dev_mode()
    env_vars: list[str] = [
        "IS_DEV_MODE",
        "VOICEVOX_URL",
        "OPENAI_API_KEY",
        "VOICEVOX_API_KEY",
        "OPENAI_ASSISTANT_ID",
        "OPENAI_THREAD_ID",
        "AZURE_STORAGE_ACCOUNT",
        "AZURE_SAS_TOKEN",
        "PUBSUB_CONNECTION_STRING",
    ]
    env_vars_prod: list[str] = [
        # 本番環境のみで使う環境変数
        "DB_NAME",
        "DB_HOST",
        "DB_USERNAME",
        "DB_PASSWORD",
        "DB_CERT_PATH",
    ]
    if not is_dev_mode:
        env_vars.extend(env_vars_prod)
    missing_vars = [var for var in env_vars if os.getenv(var) is None]
    if missing_vars:
        raise EnvironmentError(
            f"Missing environment variables: {', '.join(missing_vars)}"
        )


def get_is_dev_mode() -> bool:
    is_dev_mode = os.getenv("IS_DEV_MODE")
    return int(is_dev_mode) == 1


def get_voicevox_url():
    return os.getenv("VOICEVOX_URL")


def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")


def get_voicevox_api_key():
    return os.getenv("VOICEVOX_API_KEY")


def get_openai_assistant_id():
    return os.getenv("OPENAI_ASSISTANT_ID")


def get_openai_assistant_id_paraphrase():
    return os.getenv("OPENAI_ASSISTANT_ID_PARAPHRASE")

def get_openai_thread_id():
    return os.getenv("OPENAI_THREAD_ID")


def get_azure_storage_account():
    return os.getenv("AZURE_STORAGE_ACCOUNT")


def get_azure_sas_token():
    return os.getenv("AZURE_SAS_TOKEN")


def get_db_object() -> Dict[str, str]:
    obj = {
        "username": os.getenv("DB_USERNAME"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
    }
    return obj


def get_db_cert_path():
    return os.getenv("DB_CERT_PATH")


def get_pubsub_connection_string():
    return os.getenv("PUBSUB_CONNECTION_STRING")
