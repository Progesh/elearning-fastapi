from functools import lru_cache

from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

_ALLOWED_ALGORITHMS = {"HS256", "HS384", "HS512"}


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    DB_HOST: str = "db"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "elearning"

    API_CLIENT_ID: str = "client"
    API_CLIENT_SECRET: str = "secret"
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 60

    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters")
        return value

    @field_validator("JWT_ALGORITHM")
    @classmethod
    def validate_algorithm(cls, value: str) -> str:
        if value not in _ALLOWED_ALGORITHMS:
            raise ValueError(f"JWT_ALGORITHM must be one of {_ALLOWED_ALGORITHMS}")
        return value

    @property
    def DATABASE_URL(self) -> str:
        password = quote_plus(self.DB_PASSWORD)
        return f"mysql+pymysql://{self.DB_USER}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
