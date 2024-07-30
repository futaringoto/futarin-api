import os

def check_env_variables():
    is_dev_mode:bool = get_is_dev_mode()
    env_vars:list[str] = [
        "OPENAI_API_KEY",
        "VOICEVOX_API_KEY",
    ]
    env_vars_prod:list[str] = [
        "STORAGE_ACCOUNT_NAME",
        "SAS_TOKEN",
    ]
    if not is_dev_mode:
        env_vars.extend(env_vars_prod)
    missing_vars = [var for var in env_vars if os.getenv(var) is None]
    if missing_vars:
        raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")

def get_is_dev_mode() -> bool:
    IS_DEV = os.getenv("DEV_MODE")
    return True if IS_DEV==1 else False

def get_voicevox_url():
    return os.getenv("VOICEVOX_URL")

def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")

def get_storage_account_name():
    return os.getenv("STORAGE_ACCOUNT_NAME")

def get_sas_token():
    return os.getenv("SAS_TOKEN")

def get_voicevox_api_key():
    return os.getenv("VOICEVOX_API_KEY")
