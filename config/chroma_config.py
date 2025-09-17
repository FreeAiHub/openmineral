"""
Конфигурация Chroma для OpenMineralHub
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings

class ChromaConfig(BaseSettings):
    """Конфигурация Chroma Cloud для OpenMineralHub"""
    
    API_KEY: str = os.getenv("CHROMA_API_KEY", "ck-5AiP5CxC5ina18h2TYNusGxe4SxNs5xf4Xeep82CbF79")
    TENANT: str = os.getenv("CHROMA_TENANT", "c74ab4c5-d45c-4b29-96ac-d995b6e9bc33")
    DATABASE: str = os.getenv("CHROMA_DATABASE", "Test")
    
    # Коллекции OpenMineralHub
    COLLECTIONS = {
        "minerals": "openmineral_minerals",
        "deals": "openmineral_deals", 
        "kyc": "openmineral_kyc",
        "risk_assessment": "openmineral_risk_docs",
        "compliance": "openmineral_compliance"
    }
    
    # Embedding настройки
    EMBEDDING_PROVIDER: str = os.getenv("CHROMA_EMBEDDING_PROVIDER", "openai")
    EMBEDDING_MODEL: str = os.getenv("CHROMA_EMBEDDING_MODEL", "text-embedding-3-small")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Сервисные параметры
    RAG_ENABLED: bool = os.getenv("RAG_ENABLED", "true").lower() == "true"
    SEARCH_RESULTS_DEFAULT: int = int(os.getenv("SEARCH_RESULTS_DEFAULT", "5"))
    
    # Кеширование (Redis)
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "false").lower() == "true"
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
    
    # Мониторинг
    MONITORING_ENABLED: bool = os.getenv("CHROMA_MONITORING", "true").lower() == "true"
    OTEL_ENABLED: bool = os.getenv("OTEL_ENABLED", "false").lower() == "true"
    OTEL_SERVICE_NAME: str = os.getenv("OTEL_SERVICE_NAME", "openmineral-chroma")
    
    @classmethod
    def validate(cls) -> bool:
        """Валидация критических параметров"""
        critical = [cls.API_KEY, cls.TENANT, cls.DATABASE]
        if any(not x for x in critical):
            raise ValueError(
                "Chroma API_KEY, TENANT и DATABASE обязательны. "
                "Настройте их в .env файле или системных переменных."
            )
        
        if cls.EMBEDDING_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError(
                "Для embedding используется OpenAI, но OPENAI_API_KEY не настроен. "
                "Добавьте OPENAI_API_KEY в .env файл."
            )
        
        return True
    
    @classmethod
    def get_connection_string(cls) -> str:
        """Строка подключения для логирования"""
        return f"Chroma Cloud: {cls.TENANT}/{cls.DATABASE}"
    
    @classmethod
    def get_embedding_config(cls) -> dict:
        """Конфигурация embedding модели"""
        if cls.EMBEDDING_PROVIDER == "openai":
            return {
                "provider": "openai",
                "model": cls.EMBEDDING_MODEL,
                "api_key": cls.OPENAI_API_KEY
            }
        elif cls.EMBEDDING_PROVIDER == "sentence_transformers":
            return {
                "provider": "sentence_transformers",
                "model": "all-MiniLM-L6-v2"
            }
        else:
            return {
                "provider": "sentence_transformers",
                "model": cls.EMBEDDING_MODEL
            }

# Создание глобальной конфигурации
chroma_config = ChromaConfig()

# Автоматическая валидация при импорте
try:
    chroma_config.validate()
    print(f"✅ Chroma Config загружен: {chroma_config.get_connection_string()}")
except ValueError as e:
    print(f"⚠️  Chroma Config ошибка: {e}")
    print("   Проверьте .env файл:")
    print("   $ cat .env | grep CHROMA")
