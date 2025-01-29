# Jupiter API Service

A microservice for interacting with Jupiter API v6, providing functionality for pool liquidity management and transaction monitoring.

## Current Features

- Pool liquidity management
  - Pool state monitoring
  - Balance tracking
  - Transaction status monitoring
- Asynchronous request processing
- Automatic retry mechanism with exponential backoff
- Rate limiting and overload protection

## Requirements

- Python 3.8+
- Redis 6+
- FastAPI
- Pydantic
- aiohttp
- uvicorn

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
uvicorn main:app --reload
```

## API Endpoints

- `GET /health` - Service health check
- `GET /wallet/{address}/balance` - Get wallet balance
- `GET /transaction/{tx_id}` - Check transaction status
- `POST /criteria/update` - Update criteria

## Development

### Project Structure
```
Meteor/
├── src/
│   ├── api.py           # Jupiter API client
│   ├── models.py        # Pydantic models
│   └── config.py        # Configuration
├── tests/
│   └── test_api.py      # Tests
└── main.py              # FastAPI application
```

### Running Tests
```bash
pytest tests/
```

## License

MIT
