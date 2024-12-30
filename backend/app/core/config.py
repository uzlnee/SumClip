from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    FRONTEND_URL: str = "http://localhost:5173"
    API_V1_STR: str = "/api/v1"
    OPENAI_API_KEY: Optional[str] = None

    DB_USER: str = "postgres"
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "youtube_analysis"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()