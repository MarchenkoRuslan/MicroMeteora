# Meteora Service API

Микросервис для взаимодействия с API Meteora, предоставляющий функционал для управления ликвидностью в пулах и мониторинга транзакций.

## Функциональные возможности

- Управление ликвидностью в пулах
  - Мониторинг состояния пулов
  - Управление диапазонами ликвидности
  - Автоматическая ребалансировка
- Мониторинг транзакций и балансов
  - Параллельное сканирование кошельков (до 300 одновременно)
  - Отслеживание статусов транзакций
  - Кэширование результатов через Redis
- Метрики и мониторинг
  - Prometheus метрики и алерты
  - Расширенное логирование
  - Healthcheck эндпоинты с проверкой Redis и API

## Технические характеристики

- Асинхронная обработка запросов (asyncio)
- Автоматический retry механизм с экспоненциальной задержкой
- Rate limiting и защита от перегрузок
- Кэширование через Redis
- Prometheus мониторинг с настраиваемыми алертами
- Docker контейнеризация
- CLI интерфейс для управления

## Требования

- Python 3.11+
- Redis 6+
- Docker и Docker Compose (опционально)
- Prometheus (для мониторинга)

## Быстрый старт

### Установка через Docker

```bash
# Клонируем репозиторий
git clone https://github.com/your-org/meteora-service
cd meteora-service

# Создаем и настраиваем .env файл
cp .env.example .env
# Отредактируйте .env файл, указав необходимые параметры

# Запускаем сервис с Redis и Prometheus
docker-compose up -d
```

### Локальная установка

```bash
# Создаем виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем сервис
python -m src.main
```

## Конфигурация

### Переменные окружения (.env)

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| METEORA_API_URL | URL API Meteora | - |
| METEORA_API_KEY | API ключ | - |
| REDIS_URL | URL Redis сервера | redis://localhost:6379 |
| LOG_LEVEL | Уровень логирования | INFO |
| MAX_CONCURRENT_REQUESTS | Лимит одновременных запросов | 50 |
| REQUEST_TIMEOUT | Таймаут запросов (сек) | 30 |

### Prometheus (.yml)

Конфигурация метрик и алертов находится в файлах:
- `prometheus.yml` - основная конфигурация
- `alerts.yml` - правила алертинга

## CLI Интерфейс

```bash
# Просмотр состояния пула
meteora pool status <pool_id>

# Обновление диапазонов ликвидности
meteora pool update-ranges <pool_id> --ranges "[-100,100,1000]"

# Запуск ребалансировки
meteora pool rebalance <pool_id>
```

## API Endpoints

### Управление пулами

#### GET /pool/{pool_id}/state
Получение состояния пула
```bash
curl http://localhost:8000/pool/{pool_id}/state
```

#### POST /pool/{pool_id}/ranges
Обновление диапазонов ликвидности
```bash
curl -X POST http://localhost:8000/pool/{pool_id}/ranges \
  -H "Content-Type: application/json" \
  -d '{
    "ranges": [
      {
        "lower_tick": -100,
        "upper_tick": 100,
        "liquidity": "1000.0"
      }
    ]
  }'
```

### Мониторинг

#### GET /metrics
Prometheus метрики
```bash
curl http://localhost:8000/metrics
```

#### GET /health
Проверка работоспособности сервиса и его компонентов
```bash
curl http://localhost:8000/health
```

## Разработка

### Запуск тестов

```bash
# Запуск всех тестов
pytest

# Запуск интеграционных тестов
pytest tests/test_integration.py

# Запуск с coverage отчетом
pytest --cov=src tests/
```

## Мониторинг

### Prometheus метрики

- `meteora_api_requests_total` - количество запросов к API
- `meteora_api_request_duration_seconds` - время выполнения запросов
- `meteora_active_connections` - активные соединения
- `meteora_pool_liquidity` - ликвидность пулов
- `meteora_errors_total` - количество ошибок

### Логирование

Логи доступны:
- В stdout контейнера при запуске через Docker
- В файле logs/app.log при локальном запуске

## Безопасность

- Все конфиденциальные данные хранятся в переменных окружения
- Реализована защита от DDoS через rate limiting
- Поддержка HTTPS
- Таймауты для всех внешних запросов
- Валидация входных данных через Pydantic

## Поддержка

При возникновении проблем:
1. Проверьте логи сервиса
2. Убедитесь в правильности конфигурации
3. Проверьте доступность Redis и API Meteora
4. Проверьте метрики в Prometheus
5. Создайте issue в репозитории проекта

## Лицензия

MIT License
