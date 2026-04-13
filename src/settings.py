from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any


class Settings(BaseSettings):
    SERVER_ADDR: str = "db"
    SERVER_PORT: int = 8000
    SERVER_TEST: bool = True

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_ADDR: str
    DB_PORT: int

    JWT_SECRET: str
    @property
    def JAM_SETTINGS(self) -> dict[str, Any]:
        return {
            "jwt": {
                "alg": "HS256",
                "secret_key": self.JWT_SECRET,
                "expire": 2600,
            },
            "starlette": {
                "header_name": "Authorization",
            }
        }

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()