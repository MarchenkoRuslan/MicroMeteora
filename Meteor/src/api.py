from typing import List
import aiohttp
import asyncio
from .models import Balance

class MeteoraAPI:
    def __init__(self):
        self.session = None
        self.base_url = "https://quote-api.jup.ag/v6"
        self._loop = None

    @property
    def loop(self):
        if self._loop is None:
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
        return self._loop

    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(loop=self.loop)
        return self.session

    async def get_pools(self):
        try:
            session = await self._get_session()
            # Создаем тестовый пул для отладки
            test_pool = {
                'address': "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK",
                'liquidity': "1000000000",
                'token0': "So11111111111111111111111111111111111111112",
                'name': 'Meteora Test Pool',
                'symbol': 'MTR',
                'decimals': 9
            }
            return [test_pool]
        except Exception as e:
            print(f"Error getting pools: {str(e)}")  # Отладка
            raise Exception(f"Failed to get pools: {str(e)}")

    async def get_balance(self, address: str) -> Balance:
        try:
            pools_data = await self.get_pools()
            if not pools_data:
                raise Exception("Empty pools data received")
                
            print(f"Got pools data: {pools_data}")  # Отладка
            
            pool_info = next((pool for pool in pools_data if pool.get('address') == address), None)
            
            if pool_info:
                print(f"Found pool info: {pool_info}")  # Отладка
                return Balance(
                    address=address,
                    amount=float(pool_info.get('liquidity', 0)),
                    token_address=pool_info.get('token0', ''),
                    token_name=pool_info.get('name', ''),
                    token_symbol=pool_info.get('symbol', ''),
                    decimals=pool_info.get('decimals', 9)
                )
            else:
                raise Exception(f"Pool {address} not found in pools list")
        except Exception as e:
            print(f"Error in get_balance: {e}")  # Отладка
            raise

    async def get_balances(self, addresses: List[str]) -> List[Balance]:
        balances = []
        try:
            for address in addresses:
                try:
                    balance = await self.get_balance(address)
                    balances.append(balance)
                    print(f"Added balance for {address}: {balance}")  # Отладка
                except Exception as e:
                    print(f"Error getting balance for {address}: {e}")
        except Exception as e:
            print(f"Error in get_balances: {e}")
        
        print(f"Final balances list: {balances}")  # Отладка
        return balances

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None 