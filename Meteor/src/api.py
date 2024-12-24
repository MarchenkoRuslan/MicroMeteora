import httpx
import asyncio
from typing import List, Dict
from .models import Balance, Transaction, CriteriaUpdate, LiquidityRange, PoolState
from .config import settings
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from asyncio import Semaphore
from .exceptions import (
    MeteoraAPIError,
    RateLimitError,
    PoolNotFoundError,
    InsufficientLiquidityError
)
from .cache import Cache

logger = logging.getLogger(__name__)

class MeteoraAPI:
    def __init__(self):
        self.cache = Cache()
        self.base_url = settings.METEORA_API_URL
        self.headers = {
            "Authorization": f"Bearer {settings.METEORA_API_KEY}",
            "Content-Type": "application/json"
        }
        self.client = httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT,
            limits=httpx.Limits(
                max_connections=settings.MAX_CONCURRENT_REQUESTS,
                max_keepalive_connections=20
            )
        )
        self.semaphore = Semaphore(settings.MAX_CONCURRENT_REQUESTS)
        
    async def scan_wallets(self, wallet_addresses: List[str]) -> Dict[str, Balance]:
        """Сканирование балансов нескольких кошельков параллельно"""
        tasks = [self.get_balance(address) for address in wallet_addresses]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        balances = {}
        for address, result in zip(wallet_addresses, results):
            if isinstance(result, Exception):
                logger.error(f"Error scanning wallet {address}: {str(result)}")
                continue
            balances[address] = result
        return balances
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry_error_callback=lambda retry_state: None
    )
    async def get_balance(self, address: str) -> dict:
        # Заглушка для демонстрации
        return {
            "address": address,
            "amount": 100.0,
            "currency": "ETH"
        }

    async def check_transaction(self, tx_id: str) -> dict:
        # Заглушка для демонстрации
        return {
            "tx_id": tx_id,
            "status": "completed",
            "amount": 1.0,
            "from_address": "0x123",
            "to_address": "0x456"
        }

    async def update_criteria(self, criteria) -> dict:
        # Заглушка для демонстрации
        return {
            "status": "updated",
            "criteria_id": criteria.criteria_id
        }

    async def get_pool_state(self, pool_id: str) -> PoolState:
        """Получение текущего состояния пула"""
        async with self.semaphore:
            try:
                response = await self.client.get(
                    f"{self.base_url}/pools/{pool_id}/state",
                    headers=self.headers
                )
                response.raise_for_status()
                return PoolState(**response.json())
            except Exception as e:
                logger.error(f"Error getting pool state for {pool_id}: {e}")
                raise

    async def update_liquidity_ranges(
        self, 
        pool_id: str, 
        ranges: List[LiquidityRange]
    ) -> dict:
        """Обновление диапазонов ликвидности"""
        try:
            response = await self.client.post(
                f"{self.base_url}/pools/{pool_id}/ranges",
                headers=self.headers,
                json={"ranges": [r.dict() for r in ranges]}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error updating liquidity ranges: {e}")
            raise

    async def rebalance_pool(self, pool_id: str) -> dict:
        """Запуск ребалансировки пула"""
        try:
            response = await self.client.post(
                f"{self.base_url}/pools/{pool_id}/rebalance",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error rebalancing pool: {e}")
            raise

    async def close(self):
        await self.client.aclose()
        await self.cache.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close() 