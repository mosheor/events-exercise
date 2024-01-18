import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_CONNECTION_STRING: str = os.getenv("DB_CONNECTION_STRING", "mongodb://root:password@localhost:27017")
    DEFAULT_CONFIG_JSON_PATH: str = os.getenv(
        "DEFAULT_CONFIG_JSON_PATH", str(Path(__file__).parent / "configurations.json")
    )
