import os

from sqlalchemy import select, update, and_
from sqlalchemy.exc import IntegrityError, NoResultFound

import utils.blockchain
from utils.base import get_session, async_session
from utils.models import DepositeWallets, DepositsTransactions
from sqlalchemy.ext.asyncio import AsyncSession
from utils.models import DepositeWallets, DepositsTransactions, MainWalletTransaction
from simplecrypt import encrypt, decrypt
from decimal import Decimal



PASSWORD = os.getenv('PASSWORD')


async def add_wallet_to_db(session: AsyncSession, address: str, private_key: bytes) -> None:
    encrypt_pass = encrypt(PASSWORD, private_key)
    session.add(DepositeWallets(address=address, private_key=encrypt_pass))
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise


async def get_wallet_key(session: AsyncSession, address: str) -> str:
    try:
        results = await session.execute(select(DepositeWallets.private_key).where(
            DepositeWallets.address == address)
        )
        results = results.scalar_one()
        wallet_key = decrypt(PASSWORD, results)

        return wallet_key
    except NoResultFound:
        await session.rollback()


async def get_all_depo_wallets(session: AsyncSession) -> list:

    query = select(DepositeWallets.address)
    result = await session.execute(query)
    result = result.scalars().all()

    return result


async def add_trans(session, from_wallet, to_address, amount, currency, tx_id):

    amount = utils.blockchain.w3.fromWei(amount, 'ether')
    if from_wallet == utils.blockchain.MAIN_WALLET_ADDRESS:
        session.add(MainWalletTransaction(amount=amount, to_address=to_address, tx_id=tx_id, currency=currency))
    else:

        try:
            depo_wallet = await session.execute(select(DepositeWallets).where(DepositeWallets.address == from_wallet))
            depo_wallet = depo_wallet.scalar_one()
            session.add(DepositsTransactions(amount=amount,
                                             to_address=to_address,
                                             tx_id=tx_id,
                                             currency=currency,
                                             depositewallets=depo_wallet))
        except NoResultFound:
            await session.rollback()
            raise

    await session.commit()


async def get_transactions(session, request):
    filters = []
    if request.wallet_address is None or request.wallet_address == utils.blockchain.MAIN_WALLET_ADDRESS:
        if request.currency:
            filters.append(MainWalletTransaction.currency == request.currency)
        if request.amount:
            filters.append(MainWalletTransaction.amount >= Decimal(request.amount))
        try:
            results = await session.execute(select(MainWalletTransaction).where(and_(*filters)))
            results = results.scalars().all()
            return results
        except NoResultFound:
            return "no result"
    else:
        if request.currency:
            filters.append(DepositsTransactions.currency == request.currency)
        if request.amount:
            filters.append(DepositsTransactions.amount >= Decimal(request.amount))
        try:
            # TODO: create query one to many, remove everywhere "no result"
            wal_id = await session.execute(select(DepositeWallets.id).where(
                DepositeWallets.address == request.wallet_address)
            )
            wal_id = wal_id.scalar_one()
            filters.append(DepositsTransactions.depositewallets_id == wal_id)
            results = await session.execute(select(DepositsTransactions).where(and_(*filters)))
            results = results.scalars().all()
        except NoResultFound:
            return "no result"
        return results
