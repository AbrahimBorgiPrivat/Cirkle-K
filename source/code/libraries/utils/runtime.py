import json
import os

from libraries.utils import env


def load_runtime_vars(JSON_PATH: str):
    with open(JSON_PATH, "r", encoding="utf-8") as file:
        config = json.load(file)

    def resolve_env_vars(obj):
        if isinstance(obj, dict):
            return {key: resolve_env_vars(value) for key, value in obj.items()}
        if isinstance(obj, list):
            return [resolve_env_vars(value) for value in obj]
        if isinstance(obj, str):
            if hasattr(env, obj):
                return getattr(env, obj)
            return os.getenv(obj, obj)
        return obj

    return resolve_env_vars(config)
