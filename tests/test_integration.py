import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_pools():
    """Test getting quote from Jupiter"""
    response = client.get("/pools")
    assert response.status_code == 200
    data = response.json()
    # Проверяем поля из Jupiter API quote
    assert isinstance(data, dict)
    assert 'inputMint' in data
    assert 'outputMint' in data
    assert 'outAmount' in data

def test_get_balance():
    """Test getting token balance/price"""
    # Тестируем с SOL
    sol_address = "So11111111111111111111111111111111111111112"
    response = client.get(f"/balance/{sol_address}")
    assert response.status_code == 200
    data = response.json()
    print(f"Balance response: {data}")  # Для отладки
    
    # Проверяем основные поля
    assert data["address"] == sol_address
    assert isinstance(data["amount"], (int, float))
    assert data["token_symbol"] is not None
    assert data["decimals"] is not None

def test_get_balances():
    """Test getting multiple token balances"""
    addresses = [
        "So11111111111111111111111111111111111111112",  # SOL
        "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
    ]
    response = client.post("/balances", json=addresses)
    assert response.status_code == 200
    data = response.json()
    print(f"Balances response: {data}")  # Для отладки
    
    # Проверяем список балансов
    assert isinstance(data, list)
    assert len(data) == len(addresses)
    
    # Проверяем каждый баланс
    for balance in data:
        assert isinstance(balance, dict)
        assert "address" in balance
        assert "amount" in balance
        assert "token_symbol" in balance
        assert isinstance(balance["amount"], (int, float))

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Jupiter API Service"} 