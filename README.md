# Jupiter API Service

A microservice for interacting with Jupiter API v6, providing functionality for token swaps, price quotes, and transaction monitoring.

## Current Features

- Token price and quote management
  - Real-time price quotes
  - Token balance tracking
  - Transaction status monitoring
- Asynchronous request processing
- Automatic retry mechanism
- Rate limiting and overload protection

## Requirements

- Python 3.8+
- FastAPI
- Pydantic
- aiohttp
- uvicorn
- pytest (for testing)

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run Service

```bash
uvicorn src.main:app --reload
```

## API Endpoints

- `GET /health` - Service health check
- `GET /pools` - Get Jupiter pools and quotes
- `GET /balance/{address}` - Get token balance/price
- `POST /balances` - Get multiple token balances
- `GET /transaction/{tx_id}` - Check transaction status
- `POST /criteria/update` - Update criteria

## Development

### Project Structure
```
Jupiter/
├── src/
│   ├── api.py           # Jupiter API client
│   ├── models.py        # Pydantic models
│   └── config.py        # Configuration
├── tests/
│   ├── test_api.py      # Unit tests
│   └── test_integration.py  # Integration tests
└── main.py              # FastAPI application
```

### Running Tests
```bash
pytest -v tests/
```

## License

MIT
