import pytest
import asyncio
from decimal import Decimal
from src.api import MeteoraAPI
from src.models import LiquidityRange, PoolState

@pytest.mark.integration
class TestMeteoraIntegration:
    @pytest.fixture(autouse=True)
    async def setup(self):
        self.api = MeteoraAPI()
        yield
        await self.api.close()

    async def test_pool_lifecycle(self):
        # Создаем диапазоны ликвидности
        ranges = [
            LiquidityRange(
                lower_tick=-100,
                upper_tick=100,
                liquidity=Decimal("1000.0")
            )
        ]
        
        # Получаем состояние пула
        pool_state = await self.api.get_pool_state("test_pool")
        assert isinstance(pool_state, PoolState)
        
        # Обновляем диапазоны
        result = await self.api.update_liquidity_ranges("test_pool", ranges)
        assert result["status"] == "success"
        
        # Проверяем ребалансировку
        rebalance = await self.api.rebalance_pool("test_pool")
        assert rebalance["status"] == "success" 