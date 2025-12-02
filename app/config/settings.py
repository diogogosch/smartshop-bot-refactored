"""Application Settings using Pydantic"""
import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application configuration settings"""
    
    # Telegram
    telegram_token: str = Field(..., description="Telegram bot token")
    
    # Database
    database_url: str = Field(
        default="postgresql://smartshop:password@localhost:5432/smartshop_db",
        description="Database connection URL"
    )
    database_pool_size: int = Field(default=10, description="Database connection pool size")
    database_pool_recycle: int = Field(default=3600, description="Database connection recycle time")
    database_password: str = Field(default="password", description="Database password")
    
    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    redis_max_memory: str = Field(default="512mb", description="Redis max memory")
    
    # API Keys
    openai_api_key: str = Field(default="", description="OpenAI API key")
    google_vision_api_key: str = Field(default="", description="Google Vision API key")
    
    # Application Settings
    log_level: str = Field(default="INFO", description="Logging level")
    enable_notifications: bool = Field(default=True, description="Enable notifications")
    enable_caching: bool = Field(default=True, description="Enable caching")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Load settings
settings = Settings()
