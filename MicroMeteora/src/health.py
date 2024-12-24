from typing import Dict
from .api import MeteoraAPI
from .config import settings
from redis.asyncio import Redis

async def check_redis() -> Dict[str, bool]:
    try:
        redis = Redis.from_url(settings.REDIS_URL)
        await redis.ping()
        await redis.close()
        return {"redis": True}
    except Exception:
        return {"redis": False}

async def check_api() -> Dict[str, bool]:
    try:
        async with MeteoraAPI() as api:
            await api.health_check()
            return {"api": True}
    except Exception:
        return {"api": False}

async def health_check() -> Dict[str, bool]:
    redis_status = await check_redis()
    api_status = await check_api()
    return {
        **redis_status,
        **api_status,
        "status": all([*redis_status.values(), *api_status.values()])
    } 