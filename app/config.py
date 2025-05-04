import os

from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    model_config = ConfigDict(from_attributes=True)

    SECRET_KEY_ACCESS: str = os.getenv("SECRET_KEY_ACCESS")
    SECRET_KEY_REFRESH: str = os.getenv("SECRET_KEY_REFRESH")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TIME_TOKEN: int = int(os.getenv("ACCESSTIMETOKEN"))
    REFRESH_TOKEN_EXPIRATION: int = int(os.getenv("REFRESHTOKENEXPIRATION"))

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"



settings = Settings()



