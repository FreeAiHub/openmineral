from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application settings
    app_name: str = "OpenMineral Trading Platform"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database settings
    postgresql_url: str = "postgresql://user:password@localhost:5432/openmineral"
    mongodb_url: str = "mongodb://localhost:27017/openmineral"
    redis_url: str = "redis://localhost:6379/0"
    
    # Authentication settings
    secret_key: str = "openmineral-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI settings
    openai_api_key: Optional[str] = None
    cursor_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()