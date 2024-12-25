from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Balance(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    address: str
    amount: float = Field(default=0.0)
    token_address: Optional[str] = None
    token_name: Optional[str] = None
    token_symbol: Optional[str] = None
    decimals: int = Field(default=9)

class Transaction(BaseModel):
    tx_id: str
    status: str
    amount: float
    from_address: str
    to_address: str

class CriteriaUpdate(BaseModel):
    criteria_id: str
    value: float 

class LiquidityRange(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    min_value: float = Field(default=0.0)
    max_value: float = Field(default=float('inf'))

class PoolState(BaseModel):
    pool_id: str
    liquidity: float
    token0_balance: float
    token1_balance: float
    current_price: float 