from pydantic_settings import BaseSettings
import os
from jam import Jam


class Settings(BaseSettings):
    SERVER_ADDR: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    SERVER_TEST: bool = True

    DB_USERNAM = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_ADDR = os.getenv('DB_ADDR')
    DB_PORT = os.getenv('DB_PORT')

    JAM_SETTINGS = {
        "alg": "HS256",
        "secret_key": "secret",
        "expire": 2600
    }


settings = Settings()
