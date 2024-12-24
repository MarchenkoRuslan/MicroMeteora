import pytest
from httpx import AsyncClient
from decimal import Decimal

from src.main import app
from src.models import Balance, Transaction, CriteriaUpdate
from src.api import MeteoraAPI

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_get_wallet_balance():
    test_address = "0x1234567890abcdef"
    expected_balance = Balance(
        wallet_address=test_address,
        amount=Decimal("100.0"),
        currency="ETH"
    )
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/wallet/{test_address}/balance")
        assert response.status_code == 200
        balance = Balance(**response.json())
        assert balance.wallet_address == expected_balance.wallet_address 

@pytest.mark.asyncio
async def test_get_balance():
    api = MeteoraAPI()
    try:
        balance = await api.get_balance("test_wallet")
        assert isinstance(balance, Balance)
    finally:
        await api.close()

@pytest.mark.asyncio
async def test_batch_balance_scan():
    api = MeteoraAPI()
    try:
        wallets = ["wallet1", "wallet2", "wallet3"]
        balances = await api.get_balances(wallets)
        assert len(balances) <= len(wallets)
    finally:
        await api.close() 