import asyncio
import datetime

from pytz import timezone
from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy import String, DECIMAL
from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship

from utils.base import Base, init_models

TIMEZONE = timezone('Europe/Kiev')


def time_now():
    return datetime.datetime.now(TIMEZONE)


class MainWalletTransaction(Base):
    __tablename__ = "mainwallet_transaction"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    creation_time = Column('creation_time', DateTime(timezone=True), default=time_now())
    amount = Column(DECIMAL)
    currency = Column(String)
    to_address = Column(String)
    tx_id = Column(String)


class DepositeWallets(Base):
    __tablename__ = "depositewallets"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    creation_time = Column('creation_time', DateTime(timezone=True), default=time_now())
    address = Column(String, unique=True)
    private_key = Column(BYTEA)
    transactions = relationship('DepositsTransactions', backref='depositewallets', lazy='dynamic')


class DepositsTransactions(Base):
    __tablename__ = "deposits_transactions"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    creation_time = Column('creation_time', DateTime(timezone=True), default=time_now())
    amount = Column(DECIMAL)
    currency = Column(String)
    to_address = Column(String)
    tx_id = Column(String)
    depositewallets_id = Column(Integer, ForeignKey('depositewallets.id'))


if __name__ == "__main__":
    asyncio.run(init_models())

# run python -m utils.models
