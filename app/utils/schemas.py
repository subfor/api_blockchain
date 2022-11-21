from typing import Optional

from pydantic import BaseModel


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
