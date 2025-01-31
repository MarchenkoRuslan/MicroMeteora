from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from typing import List
import logging
import asyncio

from .api import JupiterAPI
from .models import Balance, Transaction, CriteriaUpdate
from .config import settings

# Настройка логирования
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager для FastAPI"""
    # Startup
    logger.info("Starting up...")
    # Создаем event loop если его нет
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    yield
    # Shutdown
    logger.info("Shutting down...")

app = FastAPI(
    title="Jupiter API Service",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Jupiter API Service"}

@app.get("/pools")
async def get_pools():
    """Get pools information from Jupiter"""
    api = JupiterAPI()
    try:
        return await api.get_pools()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await api.close()

@app.get("/balance/{address}")
async def get_balance(address: str):
    """Get balance for specific address"""
    api = JupiterAPI()
    try:
        return await api.get_balance(address)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await api.close()

@app.post("/balances")
async def get_balances(addresses: List[str]):
    """Get balances for multiple addresses"""
    api = JupiterAPI()
    try:
        return await api.get_balances(addresses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await api.close()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/transaction/{tx_id}", response_model=Transaction)
async def check_transaction(tx_id: str):
    api = JupiterAPI()  # Создаем экземпляр API
    try:
        transaction = await api.check_transaction(tx_id)
        return transaction
    except Exception as e:
        logger.error(f"Error checking transaction {tx_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await api.close()

@app.post("/criteria/update")
async def update_criteria(criteria: CriteriaUpdate):
    api = JupiterAPI()  # Создаем экземпляр API
    try:
        result = await api.update_criteria(criteria)
        return result
    except Exception as e:
        logger.error(f"Error updating criteria: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await api.close() 