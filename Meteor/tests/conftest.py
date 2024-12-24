import pytest
import sys
import os

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