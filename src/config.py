from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    METEORA_API_URL: str = "https://dlmm-api.meteora.ag"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_TTL: int = 300  # в секундах

    # Logging Configuration
    LOG_LEVEL: str = "INFO"

    # Monitoring
    PROMETHEUS_PORT: int = 9090

    # Rate Limiting
    RATE_LIMIT_CALLS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # в секундах

    class Config:
        env_file = ".env"
        case_sensitive = True

# Создаем экземпляр настроек
settings = Settings() 