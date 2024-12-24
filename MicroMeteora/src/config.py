from pydantic_settings import BaseSettings
from typing import Optional
from decimal import Decimal

class Settings(BaseSettings):
    METEORA_API_URL: str
    METEORA_API_KEY: str
    LOG_LEVEL: str = "INFO"
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: Optional[str] = None
    
    # API limits
    MAX_CONCURRENT_REQUESTS: int = 50
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    
    # DLMM settings
    DEFAULT_FEE_TIER: int = 3000  # 0.3%
    MIN_LIQUIDITY_AMOUNT: Decimal = Decimal("0.1")
    REBALANCE_THRESHOLD: Decimal = Decimal("0.05")  # 5%
    
    class Config:
        env_file = ".env"

settings = Settings() 