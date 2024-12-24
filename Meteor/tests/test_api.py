import sys
from pathlib import Path

# Добавляем путь к корневой директории проекта
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

import pytest
from httpx import AsyncClient
from decimal import Decimal

# Важно: импортируем app именно так
from main import app
from src.api import MeteoraAPI
from src.models import Balance

# Используем тестовый пул, который мы знаем, что существует
TEST_POOL_ADDRESS = "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK"

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_get_wallet_balance():
    api = MeteoraAPI()
    try:
        balance = await api.get_balance(TEST_POOL_ADDRESS)
        print(f"Balance response: {balance}")
        assert isinstance(balance, Balance)
        assert balance.address == TEST_POOL_ADDRESS
    finally:
        await api.close()

@pytest.mark.asyncio
async def test_get_balance():
    api = MeteoraAPI()
    try:
        balance = await api.get_balance(TEST_POOL_ADDRESS)
        print(f"Balance data: {balance}")
        assert isinstance(balance, Balance)
        assert balance.address is not None
    finally:
        await api.close()

@pytest.mark.asyncio
async def test_batch_balance_scan():
    api = MeteoraAPI()
    try:
        addresses = [
            TEST_POOL_ADDRESS,
            TEST_POOL_ADDRESS
        ]
        balances = await api.get_balances(addresses)
        print(f"Batch balances: {balances}")
        assert len(balances) == len(addresses)
        assert all(isinstance(b, Balance) for b in balances)
    finally:
        await api.close() 