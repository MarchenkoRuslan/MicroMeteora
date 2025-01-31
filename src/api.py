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

class JupiterAPI:
    def __init__(self):
        self.session = None
        self.base_url = "https://quote-api.jup.ag"
        self._loop = None

    def _get_loop(self):
        """Get or create event loop safely"""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop

    async def _get_session(self):
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            connector = aiohttp.TCPConnector(ssl=False)
            self._loop = self._get_loop()
            self.session = aiohttp.ClientSession(
                loop=self._loop,
                timeout=timeout,
                connector=connector,
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            )
        return self.session

    async def _make_request(self, url: str, params: dict = None):
        try:
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    text = await response.text()
                    raise Exception(f"Request failed: {response.status}, {text}")
        except Exception as e:
            print(f"Request error: {str(e)}")
            raise

    async def get_balance(self, address: str) -> Balance:
        """Get token info by address"""
        try:
            # Сначала получаем информацию о токене
            token_url = "https://token.jup.ag/strict"
            token_list = await self._make_request(token_url)
            token_info = next((token for token in token_list if token['address'] == address), None)
            
            if not token_info:
                raise Exception(f"Token info not found for address: {address}")
            
            # Для получения цены используем пару с USDC
            usdc_address = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
            quote_params = {
                "inputMint": address if address != usdc_address else "So11111111111111111111111111111111111111112",
                "outputMint": usdc_address if address != usdc_address else address,
                "amount": "1000000"
            }
            
            quote_url = f"{self.base_url}/v6/quote"
            quote_info = await self._make_request(quote_url, params=quote_params)
            
            # Вычисляем цену на основе quote
            price = float(quote_info.get('outAmount', 0)) / (10 ** token_info.get('decimals', 9))
            
            return Balance(
                address=address,
                amount=price,
                token_address=address,
                token_name=token_info.get('name', ''),
                token_symbol=token_info.get('symbol', ''),
                decimals=token_info.get('decimals', 9)
            )
        except Exception as e:
            print(f"Error in get_balance: {e}")
            raise

    async def get_balances(self, addresses: List[str]) -> List[Balance]:
        """Get multiple token balances"""
        balances = []
        for address in addresses:
            try:
                balance = await self.get_balance(address)
                balances.append(balance)
            except Exception as e:
                print(f"Error getting balance for {address}: {e}")
                balances.append(Balance(
                    address=address,
                    amount=0,
                    token_address=address,
                    token_name='Unknown',
                    token_symbol='Unknown',
                    decimals=9
                ))
        return balances

    async def get_pools(self):
        """Get quote from Jupiter API"""
        try:
            url = f"{self.base_url}/v6/quote"
            params = {
                "inputMint": "So11111111111111111111111111111111111111112",  # SOL
                "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
                "amount": "100000000",  # 0.1 SOL
                "slippageBps": "50"
            }
            
            data = await self._make_request(url, params=params)
            return data
        except Exception as e:
            print(f"Error getting quote: {str(e)}")
            raise

    async def close(self):
        """Close session and cleanup"""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None
        if self._loop:
            self._loop = None 