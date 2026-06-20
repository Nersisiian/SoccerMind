from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    SECRET_KEY: str = "super_secret_key_change_me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: str = "postgresql+asyncpg://soccermind:soccermind_pass@postgres:5432/soccermind"
    REDIS_URL: str = "redis://redis:6379/0"

    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    STRIPE_API_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_MONTHLY: str = ""
    STRIPE_PRICE_YEARLY: str = ""

    class Config:
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == "CORS_ORIGINS":
                return json.loads(raw_val)
            return raw_val

settings = Settings()