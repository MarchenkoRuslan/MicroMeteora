from typing import Any, Optional
from redis.asyncio import Redis
from .config import settings

class Cache:
    def __init__(self):
        self.redis = Redis.from_url(settings.REDIS_URL)

    async def get(self, key: str) -> Optional[Any]:
        return await self.redis.get(key)

    async def set(self, key: str, value: Any, expire: int = 60):
        await self.redis.set(key, value, ex=expire)

    async def close(self):
        await self.redis.close() 