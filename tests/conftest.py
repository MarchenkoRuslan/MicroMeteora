import pytest
import sys
import os
import aiohttp
from unittest.mock import AsyncMock, MagicMock

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Регистрируем маркер integration
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )

# Устанавливаем asyncio как маркер по умолчанию для всех тестов
pytest_plugins = ['pytest_asyncio'] 

@pytest.fixture
def mock_pool_response():
    return {
        "address": "8JJSdD1kKieGdXGRBmV4SxXbEGQYtKrqKZGBH9Kw3GBf",
        "liquidity": "1000000000",
        "token0": "So11111111111111111111111111111111111111112",
        "name": "Test Pool",
        "symbol": "TEST",
        "decimals": 9
    }

@pytest.fixture
def mock_aiohttp_session(mock_pool_response):
    async def mock_get(*args, **kwargs):
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=mock_pool_response)
        return mock_response

    session = AsyncMock()
    session.get = mock_get
    session.close = AsyncMock()
    return session 