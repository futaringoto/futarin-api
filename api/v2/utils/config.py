import os


def check_env_variables():
    is_dev_mode: bool = get_is_dev_mode()
    env_vars: list[str] = [
        "OPENAI_API_KEY",
        "VOICEVOX_API_KEY",
    ]
    env_vars_prod: list[str] = []
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


def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")


def get_voicevox_api_key():
    return os.getenv("VOICEVOX_API_KEY")


def get_async_db_url():
    password = os.getenv("MYSQL_ROOT_PASSWORD")
    db_name = os.getenv("MYSQL_DATABASE")
    url = f"mysql+aiomysql://root:{password}@mysql:3306/{db_name}?charset=utf8"
    return url


def get_db_url():
    password = os.getenv("MYSQL_ROOT_PASSWORD")
    db_name = os.getenv("MYSQL_DATABASE")
    url = f"mysql+pymysql://root:{password}@mysql:3306/{db_name}?charset=utf8"
    return url


def get_azure_sas_token():
    return os.getenv("AZURE_SAS_TOKEN")