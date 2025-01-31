import pytest
from src.api import JupiterAPI

# Убираем тесты Meteora, оставляем только Jupiter
@pytest.mark.asyncio
async def test_jupiter_get_pools():
    api = JupiterAPI()
    try:
        pools = await api.get_pools()
        print(f"Jupiter pools response: {pools}")
        assert pools is not None
        # Проверяем наличие ключевых полей в ответе
        assert 'outAmount' in pools
        assert 'priceImpactPct' in pools
    finally:
        await api.close()

@pytest.mark.asyncio
async def test_jupiter_get_balance():
    api = JupiterAPI()
    try:
        # Используем адрес SOL токена
        balance = await api.get_balance("So11111111111111111111111111111111111111112")
        assert balance is not None
        assert balance.amount > 0
        assert balance.token_symbol == "SOL"
    finally:
        await api.close()

@pytest.mark.asyncio
async def test_jupiter_get_balances():
    api = JupiterAPI()
    addresses = [
        "So11111111111111111111111111111111111111112",  # SOL
        "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
    ]
    try:
        balances = await api.get_balances(addresses)
        assert len(balances) == len(addresses)
        for balance in balances:
            assert balance.amount >= 0
    finally:
        await api.close() 