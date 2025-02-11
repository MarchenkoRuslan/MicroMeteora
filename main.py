from fastapi import FastAPI, HTTPException, Depends
from typing import List
import logging

from src.api import MeteoraAPI
from src.models import Balance, Transaction, CriteriaUpdate
from src.config import settings

# Настройка логирования
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Инициализация FastAPI с метаданными
app = FastAPI(
    title="Meteora Service API",
    description="API for interacting with Meteora liquidity pools",
    version="1.0.0"
)

# Создаем единственный экземпляр API
meteora_api = MeteoraAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/wallet/{address}/balance", response_model=Balance)
async def get_wallet_balance(address: str):
    try:
        balance = await meteora_api.get_balance(address)
        return balance
    except Exception as e:
        logger.error(f"Error getting balance for wallet {address}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transaction/{tx_id}", response_model=Transaction)
async def check_transaction(tx_id: str):
    try:
        transaction = await meteora_api.check_transaction(tx_id)
        return transaction
    except Exception as e:
        logger.error(f"Error checking transaction {tx_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/criteria/update")
async def update_criteria(criteria: CriteriaUpdate):
    try:
        result = await meteora_api.update_criteria(criteria)
        return result
    except Exception as e:
        logger.error(f"Error updating criteria: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Добавляем обработчик завершения для корректного закрытия соединений
@app.on_event("shutdown")
async def shutdown_event():
    await meteora_api.close() 