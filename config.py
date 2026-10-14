import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    app_name: str = os.getenv("APP_NAME", "AegisYouth AI")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    secret_key: str = os.getenv("SECRET_KEY", "fallback_secret_key")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./aegisyouth.db")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()