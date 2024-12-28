from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    FRONTEND_URL: str = "http://localhost:5173"
    API_V1_STR: str = "/api/v1"
    OPENAI_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()