import click
import asyncio
from typing import List
import json
from decimal import Decimal
from .api import MeteoraAPI
from .models import LiquidityRange

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

@click.group()
def cli():
    """Meteora Service CLI"""
    pass

@cli.group()
def wallet():
    """Управление кошельками"""
    pass

@cli.group()
def pool():
    """Управление пулами ликвидности"""
    pass

@cli.group()
def metrics():
    """Управление метриками и мониторингом"""
    pass

@wallet.command()
@click.argument('address')
def balance(address: str):
    """Получить баланс кошелька"""
    async def get_balance():
        async with MeteoraAPI() as api:
            result = await api.get_balance(address)
            click.echo(json.dumps(result.dict(), cls=DecimalEncoder, indent=2))
    
    asyncio.run(get_balance())

@wallet.command()
@click.argument('addresses', nargs=-1)
def scan(addresses: List[str]):
    """Сканировать несколько кошельков"""
    async def scan_wallets():
        async with MeteoraAPI() as api:
            results = await api.get_balances(list(addresses))
            click.echo(json.dumps(results, cls=DecimalEncoder, indent=2))
    
    asyncio.run(scan_wallets())

@pool.command()
@click.argument('pool_id')
def state(pool_id: str):
    """Получить состояние пула"""
    async def get_state():
        async with MeteoraAPI() as api:
            result = await api.get_pool_state(pool_id)
            click.echo(json.dumps(result.dict(), cls=DecimalEncoder, indent=2))
    
    asyncio.run(get_state())

@pool.command()
@click.argument('pool_id')
def rebalance(pool_id: str):
    """Запустить ребаланс��ровку пула"""
    async def do_rebalance():
        async with MeteoraAPI() as api:
            result = await api.rebalance_pool(pool_id)
            click.echo(json.dumps(result, indent=2))
    
    asyncio.run(do_rebalance())

@metrics.command()
def show():
    """Показать текущие метрики"""
    import requests
    try:
        response = requests.get("http://localhost:8000/metrics")
        click.echo(response.text)
    except Exception as e:
        click.echo(f"Ошибка при получении метрик: {e}", err=True)

@cli.command()
def health():
    """Проверка состояния сервиса"""
    import requests
    try:
        response = requests.get("http://localhost:8000/health")
        status = response.json()
        click.echo(json.dumps(status, indent=2))
    except Exception as e:
        click.echo(f"Ошибка при проверке состояния: {e}", err=True)

if __name__ == '__main__':
    cli() 