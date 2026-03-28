from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any


class Settings(BaseSettings):
    SERVER_ADDR: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    SERVER_TEST: bool = True

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_ADDR: str
    DB_PORT: int

    JAM_SETTINGS: dict[str, Any] = {
        "auth_type": "jwt",
        "alg": "HS256",
        "secret_key": "secret",
        "expire": 2600,
        "public_key": "JAM_PUBLIC_KEY",
        "private_key": "JAM_PRIVATE_KEY",

    }

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
