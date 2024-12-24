from fastapi import FastAPI, HTTPException
from src.api import MeteoraAPI
from src.models import Balance

# Важно: определяем app как глобальную переменную
app = FastAPI(
    title="Meteor API",
    description="API for Meteor service",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/wallet/{address}/balance")
async def get_wallet_balance(address: str):
    api = MeteoraAPI()
    try:
        balance = await api.get_balance(address)
        return balance
    finally:
        await api.close() 