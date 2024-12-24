import pytest
from src.api import MeteoraAPI
from src.models import LiquidityRange

class TestMeteoraIntegration:
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_real_api_connection(self):
        api = MeteoraAPI()
        try:
            pools = await api.get_pools()
            assert pools is not None
            assert len(pools) > 0
            
            # Проверяем структуру данных пула
            pool = pools[0]
            assert 'address' in pool
            assert 'liquidity' in pool
            assert 'token0' in pool
        finally:
            await api.close()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_pool_lifecycle(self):
        api = MeteoraAPI()
        try:
            # Создаем диапазон ликвидности с значениями по умолчанию
            liquidity_range = LiquidityRange()
            assert liquidity_range.min_value == 0.0
            assert liquidity_range.max_value == float('inf')

            # Или с конкретными значениями
            custom_range = LiquidityRange(min_value=1.0, max_value=100.0)
            assert custom_range.min_value == 1.0
            assert custom_range.max_value == 100.0
        finally:
            await api.close() 