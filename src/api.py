from typing import List
import aiohttp
import asyncio
from .models import Balance
from .config import settings

class MeteoraAPI:
    def __init__(self):
        self.session = None
        self.base_url = "https://api.meteora.ag"
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
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(
                loop=self.loop,
                timeout=timeout,
                connector=aiohttp.TCPConnector(ssl=False),
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            )
        return self.session

    async def get_pools(self):
        """Get all DLMM pools"""
        try:
            session = await self._get_session()
            url = f"{self.base_url}/dlmm/pools"
            print(f"Requesting pools URL: {url}")
            
            async with session.get(url) as response:
                print(f"Pools response status: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    print(f"Pools data: {str(data)[:200]}...")
                    return data
                else:
                    text = await response.text()
                    print(f"Pools error response: {text}")
                    raise Exception(f"Failed to get pools: {response.status}, {text}")
        except Exception as e:
            print(f"Error getting pools: {str(e)}")
            raise

    async def get_balance(self, address: str) -> Balance:
        """Get pool info by address"""
        try:
            session = await self._get_session()
            url = f"{self.base_url}/dlmm/pool/{address}"
            print(f"Requesting pool URL: {url}")
            
            async with session.get(url) as response:
                print(f"Pool response status: {response.status}")
                if response.status == 200:
                    pool_info = await response.json()
                    print(f"Pool info: {pool_info}")
                    return Balance(
                        address=address,
                        amount=float(pool_info.get('tvl', 0)),
                        token_address=pool_info.get('tokenA', ''),
                        token_name=pool_info.get('tokenASymbol', ''),
                        token_symbol=pool_info.get('tokenASymbol', ''),
                        decimals=pool_info.get('tokenADecimals', 9)
                    )
                else:
                    text = await response.text()
                    print(f"Pool error response: {text}")
                    raise Exception(f"Failed to get pool info: {response.status}, {text}")
        except Exception as e:
            print(f"Error in get_balance: {e}")
            raise

    async def get_balances(self, addresses: List[str]) -> List[Balance]:
        """Get multiple pool balances"""
        balances = []
        for address in addresses:
            try:
                balance = await self.get_balance(address)
                balances.append(balance)
            except Exception as e:
                print(f"Error getting balance for {address}: {e}")
        return balances

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None 