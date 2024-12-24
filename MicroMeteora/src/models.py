from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from decimal import Decimal
from enum import Enum
from config import settings

class LiquidityRange(BaseModel):
    lower_tick: int = Field(..., description="Нижняя граница диапазона")
    upper_tick: int = Field(..., description="Верхняя граница диапазона")
    liquidity: Decimal = Field(..., gt=0, description="Объем ликвидности")

    @validator('liquidity')
    def validate_liquidity(cls, v):
        if v < settings.MIN_LIQUIDITY_AMOUNT:
            raise ValueError(f"Liquidity must be >= {settings.MIN_LIQUIDITY_AMOUNT}")
        return v

    @validator('upper_tick')
    def validate_ticks(cls, v, values):
        if 'lower_tick' in values and v <= values['lower_tick']:
            raise ValueError('upper_tick must be greater than lower_tick')
        return v

class MarketMakerType(str, Enum):
    STATIC = "static"
    DYNAMIC = "dynamic"

class CriteriaUpdate(BaseModel):
    shape: Optional[str]
    range: Optional[List[Decimal]]
    volume: Optional[Decimal]
    market_maker_type: Optional[MarketMakerType] = Field(default=MarketMakerType.DYNAMIC)
    liquidity_ranges: Optional[List[LiquidityRange]]
    rebalance_threshold: Optional[Decimal] = Field(ge=0, le=1)

class PoolState(BaseModel):
    pool_id: str
    current_tick: int
    liquidity: Decimal = Field(gt=0)
    ranges: List[LiquidityRange]
    price: Decimal = Field(gt=0)
    volume_24h: Optional[Decimal]
    fee_tier: int = Field(ge=0, le=10000)  # базисные пункты (0.01%) 