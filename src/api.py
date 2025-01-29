from typing import List
import aiohttp
import asyncio
from .models import Balance
from .config import settings

class MeteoraAPI:
    def __init__(self):
        self.session = None
        self.base_url = "https://api.meteora.ag"
        self._loop = asyncio.get_event_loop() if not asyncio.get_event_loop().is_closed() else asyncio.new_event_loop()

    async def _get_session(self):
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            connector = aiohttp.TCPConnector(ssl=False)
            self.session = aiohttp.ClientSession(
                loop=self._loop,
                timeout=timeout,
                connector=connector,
                headers={
                    'Accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0',
                    'Network': 'mainnet-beta'
                }
            )
        return self.session

    async def _make_request(self, url: str, max_retries: int = 3, initial_delay: float = 1.0):
        """Make request with retry logic"""
        for attempt in range(max_retries):
            try:
                session = await self._get_session()
                print(f"Attempt {attempt + 1} - Requesting URL: {url}")
                
                async with session.get(url) as response:
                    print(f"Response status: {response.status}")
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 503:
                        text = await response.text()
                        print(f"503 error response: {text}")
                        if attempt < max_retries - 1:
                            delay = initial_delay * (2 ** attempt)  # exponential backoff
                            print(f"Retrying after {delay} seconds...")
                            await asyncio.sleep(delay)
                            continue
                    text = await response.text()
                    raise Exception(f"Request failed: {response.status}, {text}")
            except Exception as e:
                if attempt < max_retries - 1:
                    delay = initial_delay * (2 ** attempt)
                    print(f"Error: {str(e)}. Retrying after {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    raise

    async def get_pools(self):
        """Get all pools from Meteora DLMM API"""
        try:
            url = f"{self.base_url}/api/v1/dlmm/pools"
            print(f"Requesting pools URL: {url}")
            data = await self._make_request(url)
            print(f"Pools data: {str(data)[:200]}...")
            return data
        except Exception as e:
            print(f"Error getting pools: {str(e)}")
            raise

    async def get_balance(self, address: str) -> Balance:
        """Get pool info by address from Meteora DLMM API"""
        try:
            url = f"{self.base_url}/api/v1/dlmm/pool/{address}"
            print(f"Requesting pool URL: {url}")
            pool_info = await self._make_request(url)
            print(f"Pool info: {pool_info}")
            return Balance(
                address=address,
                amount=float(pool_info.get('tvl', 0)),
                token_address=pool_info.get('tokenAMint', ''),
                token_name=pool_info.get('tokenASymbol', ''),
                token_symbol=pool_info.get('tokenASymbol', ''),
                decimals=pool_info.get('tokenADecimals', 9)
            )
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