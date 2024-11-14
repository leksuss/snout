import os
from zoneinfo import ZoneInfo

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_LOGIN: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str

    TIMEZONE: ZoneInfo = ZoneInfo('Europe/Moscow')

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')

    @property
    def DATABASE_URL(self):
        return f'postgresql+psycopg2://{self.POSTGRES_LOGIN}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}'


settings = Settings()
