import pytest
from httpx import AsyncClient
from src.models import Balance
from main import app

# Реальный адрес пула из их SDK
TEST_POOL_ADDRESS = "DLMMMg9ekmEP8HhEWpRh4dWBrPgYUkR4FkE6UF1bVpWy"

@pytest.mark.asyncio
async def test_health_check():
    """Test our service health endpoint"""
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_get_pools():
    """Test getting all pools from Meteora"""
    from src.api import MeteoraAPI
    api = MeteoraAPI()
    try:
        pools = await api.get_pools()
        print(f"Got pools: {pools[:2]}")  # Показываем первые 2 пула
        assert pools is not None
        assert len(pools) > 0
    finally:
        await api.close()

@pytest.mark.asyncio
async def test_get_wallet_balance():
    """Test getting single pool balance"""
    from src.api import MeteoraAPI
    api = MeteoraAPI()
    try:
        balance = await api.get_balance(TEST_POOL_ADDRESS)
        print(f"Got balance: {balance}")
        assert isinstance(balance, Balance)
        assert balance.address == TEST_POOL_ADDRESS
    finally:
        await api.close()

@pytest.mark.asyncio
async def test_batch_balance_scan():
    """Test getting multiple pool balances"""
    from src.api import MeteoraAPI
    api = MeteoraAPI()
    try:
        addresses = [
            TEST_POOL_ADDRESS,
            "7qbRF6YsyGuLUVs6Y1q64bdVrfe4ZcUUz1JRdoVNUJnm"  # Другой реальный пул
        ]
        balances = await api.get_balances(addresses)
        print(f"Got balances: {balances}")
        assert len(balances) > 0
        assert all(isinstance(b, Balance) for b in balances)
    finally:
        await api.close() 