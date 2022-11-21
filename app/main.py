import os
from decimal import Decimal

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_utils.tasks import repeat_every
from sqlalchemy.ext.asyncio import AsyncSession

import utils.blockchain
from utils.base import get_session
from utils.db_utils import add_wallet_to_db, get_transactions
from utils.blockchain import create_depo_wallet
from utils.blockchain import get_balance
from utils.schemas import BalanceReq, TransactionReq, TransactionFilter

API_KEY = os.getenv('API_KEY')

api_keys = [API_KEY]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )

@app.get("/")
def read_root():
    return {"home": "page"}


@app.get("/api/createwallet/", dependencies=[Depends(api_key_auth)])
async def create_wallet(session: AsyncSession = Depends(get_session)):
    created_wallet = await create_depo_wallet(session)
    return created_wallet


@app.get("/api/getbalances/", dependencies=[Depends(api_key_auth)])
async def get_balances(request: BalanceReq):
    balance = await get_balance(request=request)
    return balance


@app.post("/api/gettransactions/", dependencies=[Depends(api_key_auth)])
async def get_transaction_by_filter(request: TransactionFilter, session: AsyncSession = Depends(get_session)):
    transactions = await get_transactions(session, request=request)
    return transactions


@app.post("/api/createtransaction/", dependencies=[Depends(api_key_auth)])
async def create_transaction(request: TransactionReq, session: AsyncSession = Depends(get_session)):
    transaction = await utils.blockchain.create_transaction(session=session, request=request)
    return transaction


@app.on_event("startup")
@repeat_every(seconds=60 * 60, wait_first=True)  # 1 hour
async def transfer_balancses() -> None:
    transaction_req = TransactionReq
    balance_req = BalanceReq

    async with utils.base.async_session() as session:
        depo_wallets = await utils.db_utils.get_all_depo_wallets(session=session)

        for wallet in depo_wallets:
            balance_req.wallet_address = wallet
            balance_req.currency = None
            wallet_balance = await get_balance(request=balance_req)
            wallet_balance.reverse()

            for balance in wallet_balance:
                if Decimal(balance.get('value')) > 0:
                    transaction_req.from_wallet = wallet
                    transaction_req.to_address = utils.blockchain.MAIN_WALLET_ADDRESS
                    transaction_req.currency = balance.get('tokenSymbol')
                    transaction_req.amount = None

                    await utils.blockchain.create_transaction(session=session, request=transaction_req)
