import pytest
from src.api import MeteoraAPI
from src.models import LiquidityRange, Balance

class TestMeteoraIntegration:
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_real_api_connection(self):
        api = MeteoraAPI()
        try:
            pools = await api.get_pools()
            assert pools is not None
            assert isinstance(pools, list)
            
            if len(pools) > 0:  # Проверяем только если есть пулы
                pool = pools[0]
                # Проверяем основные поля, которые должны быть в ответе Meteora
                assert 'address' in pool
                assert 'token0' in pool
                assert 'token1' in pool  # Добавили проверку второго токена
        finally:
            await api.close()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_pool_balance(self):
        api = MeteoraAPI()
        try:
            # Получаем список пулов
            pools = await api.get_pools()
            if pools and len(pools) > 0:
                # Берем первый пул для теста
                test_pool = pools[0]
                balance = await api.get_balance(test_pool['address'])
                
                assert isinstance(balance, Balance)
                assert balance.address == test_pool['address']
                assert balance.amount is not None
                assert balance.token_address is not None
        finally:
            await api.close()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_liquidity_range(self):
        # Тест для проверки модели LiquidityRange
        liquidity_range = LiquidityRange()
        assert liquidity_range.min_value == 0.0
        assert liquidity_range.max_value == float('inf')

        custom_range = LiquidityRange(min_value=1.0, max_value=100.0)
        assert custom_range.min_value == 1.0
        assert custom_range.max_value == 100.0 