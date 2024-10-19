from typing import Literal

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')


class Settings(CustomBaseSettings):
    MODE: Literal['TEST', 'PROD', 'DEV'] = 'DEV'

    POSTGRES_NAME: str
    POSTGRES_PASS: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    DATABASE_URL: PostgresDsn | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.DATABASE_URL:
            self.DATABASE_URL = PostgresDsn.build(
                scheme='postgresql+asyncpg',
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASS,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_NAME,
            )


settings = Settings()
