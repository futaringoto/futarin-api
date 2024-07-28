import os

def check_env_variable(var_name):
    return os.getenv(var_name) is not None

if __name__ == "__main__":
    env_vars = [
        "OPENAI_API_KEY",
        "VOICEVOX_API_KEY",
        "STORAGE",
        "SAS_TOKEN"
    ]
    for env_var in env_vars:
        if check_env_variable(env_var):
            print(f"{env_var} exists.")
        else:
            print(f"{env_var} does not exist.")
