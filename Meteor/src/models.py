from pydantic import BaseModel
from typing import Optional, List

class Balance(BaseModel):
    address: str
    amount: float
    currency: str

class Transaction(BaseModel):
    tx_id: str
    status: str
    amount: float
    from_address: str
    to_address: str

class CriteriaUpdate(BaseModel):
    criteria_id: str
    value: float 