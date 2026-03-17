from pydantic_settings import BaseSettings
import os
from typing import Any


class Settings(BaseSettings):
    SERVER_ADDR: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    SERVER_TEST: bool = True

    DB_USERNAME: str = os.getenv('DB_USERNAME')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_ADDR: str = os.getenv('DB_ADDR')
    DB_PORT: str = os.getenv('DB_PORT')

    JAM_SETTINGS: dict[str, Any] = {
        "alg": "HS256",
        "secret_key": "secret",
        "expire": 2600
    }


settings = Settings()
