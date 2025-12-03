from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    OPENAI_API_KEY: str | None = None
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
        DATABASE_MAX_OVERFLOW: int = 10
    LOG_LEVEL: str = "INFO"
        HOST: str = "0.0.0.0"
    PORT: int = 8080

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
