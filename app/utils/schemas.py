from typing import Optional

from pydantic import BaseModel

tags_metadata = [
    {
        "name": "keys",
        "description": "Get all keys. **Authorization** required",
    },
    {
        "name": "managekeys",
        "description": "Add or Delete key. **Authorization** required",
    },
]


class BalanceReq(BaseModel):
    wallet_address: str
    currency: Optional[str]


class TransactionReq(BaseModel):
    from_wallet: Optional[str]
    currency: str
    amount: Optional[str]
    to_address: str


class TransactionFilter(BaseModel):
    wallet_address: Optional[str]
    currency: Optional[str]
    amount: Optional[str]
