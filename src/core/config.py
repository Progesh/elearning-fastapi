from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    DB_HOST: str = "db"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "elearning"

    @property
    def DATABASE_URL(self) -> str:
        password = quote_plus(self.DB_PASSWORD)
        return f"mysql+pymysql://{self.DB_USER}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
