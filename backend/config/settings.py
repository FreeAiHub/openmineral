"""
OpenMineral Backend Settings
Pydantic configuration loader for environment variables
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """OpenMineral Backend Configuration"""
    
    # Application
    app_name: str = "OpenMineral"
    app_version: str = "0.1.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    environment: str = os.getenv("ENVIRONMENT", "development")
    testing: bool = os.getenv("TESTING", "False").lower() == "true"
    
    # Server
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    reload: bool = os.getenv("RELOAD", "False").lower() == "true"
    
    # CORS
    cors_origins: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
    
    # Database
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db: str = os.getenv("POSTGRES_DB", "openmineral")
    postgres_user: str = os.getenv("POSTGRES_USER", "openmineral")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "devpassword")
    
    # Test Database
    test_postgres_db: str = os.getenv("TEST_POSTGRES_DB", "openmineral_test")
    
    # Redis
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    redis_password: Optional[str] = os.getenv("REDIS_PASSWORD")
    redis_db: int = int(os.getenv("REDIS_DB", "0"))
    
    # MongoDB
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    mongodb_db: str = os.getenv("MONGODB_DB", "openmineral")
    test_mongodb_db: str = os.getenv("TEST_MONGODB_DB", "openmineral_test")
    
    # Chroma Configuration
    chroma_api_key: str = os.getenv("CHROMA_API_KEY", "")
    chroma_tenant: str = os.getenv("CHROMA_TENANT", "c74ab4c5-d45c-4b29-96ac-d995b6e9bc33")
    chroma_database: str = os.getenv("CHROMA_DATABASE", "openmineral")
    chroma_test_path: str = os.getenv("CHROMA_TEST_PATH", "./chroma_test_db")
    chroma_embedding_provider: str = os.getenv("CHROMA_EMBEDDING_PROVIDER", "openai")
    chroma_embedding_model: str = os.getenv("CHROMA_EMBEDDING_MODEL", "text-embedding-3-small")
    
    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_organization: Optional[str] = os.getenv("OPENAI_ORGANIZATION")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    use_mock_ai: bool = os.getenv("USE_MOCK_AI", "False").lower() == "true"
    
    # JWT
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your_super_secret_jwt_key_here")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_token_expire_minutes: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    jwt_refresh_token_expire_days: int = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # RAG Settings
    rag_enabled: bool = os.getenv("RAG_ENABLED", "true").lower() == "true"
    search_results_default: int = int(os.getenv("SEARCH_RESULTS_DEFAULT", "5"))
    
    # Caching
    redis_enabled: bool = os.getenv("REDIS_ENABLED", "false").lower() == "true"
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Test Users
    test_user_email: str = os.getenv("TEST_USER_EMAIL", "testuser@openmineral.dev")
    test_user_password: str = os.getenv("TEST_USER_PASSWORD", "testpassword123")
    
    # Mock Services
    use_mock_market_data: bool = os.getenv("USE_MOCK_MARKET_DATA", "false").lower() == "true"
    use_mock_kyc_services: bool = os.getenv("USE_MOCK_KYC_SERVICES", "false").lower() == "true"
    use_mock_compliance_checks: bool = os.getenv("USE_MOCK_COMPLIANCE_CHECKS", "false").lower() == "true"

    # Celery
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    celery_result_backend: str = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
    celery_accept_content: List[str] = ["json"]
    celery_task_serializer: str = "json"
    celery_result_serializer: str = "json"
    celery_timezone: str = "Europe/Lisbon"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

# Global settings instance
settings = Settings()

# Validation
if settings.testing:
    print("🧪 Running in TEST mode")
    print(f"   Chroma Test Path: {settings.chroma_test_path}")
    print(f"   Mock AI: {settings.use_mock_ai}")
    print(f"   Mock Market Data: {settings.use_mock_market_data}")

if settings.debug:
    print("🐛 Running in DEBUG mode")
    print(f"   Environment: {settings.environment}")
    print(f"   Chroma Provider: {settings.chroma_embedding_provider}")

# Chroma validation
if not settings.testing and settings.chroma_api_key:
    print(f"☁️  Chroma Cloud: {settings.chroma_tenant}/{settings.chroma_database}")
elif settings.testing:
    print(f"🧪 Chroma Local: {settings.chroma_test_path}")
else:
    print("⚠️  WARNING: No Chroma configuration detected")
