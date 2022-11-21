import os
import json

from fastapi import HTTPException

import httpx
from web3 import Web3
from web3.gas_strategies.time_based import medium_gas_price_strategy, slow_gas_price_strategy, fast_gas_price_strategy
from eth_account import Account
from web3.middleware import geth_poa_middleware
from decimal import Decimal

from utils.db_utils import get_wallet_key, add_wallet_to_db, add_trans


MAIN_WALLET_ADDRESS = os.getenv('MAIN_WALLET_ADDRESS')
MAIN_WALLET_KEY = os.getenv('MAIN_WALLET_KEY')
NAITIVE_TOKEN = os.getenv('NAITIVE_TOKEN')
RPC_KEY = os.getenv('RPC_KEY')
COVAL_KEY = os.getenv('COVAL_KEY')

w3 = Web3(Web3.HTTPProvider(
    f"https://indulgent-patient-patron.bsc-testnet.discover.quiknode.pro/{RPC_KEY}/"))

w3.middleware_onion.inject(geth_poa_middleware, layer=0)


async def create_depo_wallet(session) -> dict:
    Account.enable_unaudited_hdwallet_features()
    account, mnemonic = Account.create_with_mnemonic()
    address = account.address
    await add_wallet_to_db(session,
                           address=address,
                           private_key=account.key
                           )
    data = {
        'address': address,
        'private_key': w3.toHex(account.key),
        'mnemonic': mnemonic
    }
    return data


def convert_to_decimal(value: str, token_decimal: str) -> Decimal:
    decimal_amount = Decimal(value) * 10 ** (Decimal(token_decimal) * -1)
    return decimal_amount


def convert_to_wei(value: str, token_decimal: str) -> int:
    decimal_amount = Decimal(value) * 10 ** Decimal(token_decimal)
    return int(decimal_amount)


async def get_tokens_balances(wallet_address: str) -> list:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f'https://api.covalenthq.com/v1/97/address/{wallet_address}/balances_v2/?&key={COVAL_KEY}')
        # TODO: add exeptions
        return r.json().get('data').get('items')


async def get_main_curency_balance(wallet_address: str) -> dict:
    main_curency_balance = w3.eth.getBalance(wallet_address)
    main_curency_balance = w3.fromWei(main_curency_balance, 'ether')
    balance = {"value": f"{main_curency_balance}", "tokenSymbol": NAITIVE_TOKEN}
    return balance


async def get_balance(request):
    if request.currency:
        if request.currency.upper() == NAITIVE_TOKEN:
            main_curency_balance = await get_main_curency_balance(request.wallet_address)
            return main_curency_balance
        else:
            tokens_balance = await get_tokens_balances(request.wallet_address)

            for token in tokens_balance:
                if token.get('contract_ticker_symbol') == request.currency.upper():
                    return {"value": str(convert_to_decimal(token.get('balance'), token.get('contract_decimals'))),
                            "tokenSymbol": token.get('contract_ticker_symbol')}
            raise HTTPException(status_code=404, detail="token balance not found")
    else:
        main_curency_balance = await get_main_curency_balance(request.wallet_address)
        tokens_balance = await get_tokens_balances(request.wallet_address)

        format_tokens_balance = [{
            "value": str(convert_to_decimal(token.get('balance'), token.get('contract_decimals'))),
            "tokenSymbol": token.get('contract_ticker_symbol')}
            for token in tokens_balance if token.get('contract_ticker_symbol') != NAITIVE_TOKEN]
        balance = [main_curency_balance, *format_tokens_balance]
        return balance


async def create_main_currency_transaction(from_wallet, to_wallet, gas, gas_price, amount_to_send, wallet_key):

    tx_create = w3.eth.account.signTransaction(
        {
            'chainId': 97,
            "nonce": w3.eth.get_transaction_count(from_wallet),
            "gasPrice": gas_price,
            "gas": gas,
            "to": to_wallet,
            "value": amount_to_send,
        },
        wallet_key,
    )
    tx_hash = w3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return {"tx_id": tx_receipt.transactionHash.hex()}


async def create_token_transaction(from_wallet, to_wallet, gas, gas_price, amount_to_send, wallet_key, contr_addr):
    abi = '[{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],' \
          '"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,' \
          '"stateMutability":"nonpayable","type":"function"}] '
    abi = json.loads(abi)
    contractAddress = w3.toChecksumAddress(contr_addr)
    contract = w3.eth.contract(address=contractAddress, abi=abi)
    nonce = w3.eth.getTransactionCount(from_wallet)

    token_txn = contract.functions.transfer(
        to_wallet,
        amount_to_send,

    ).buildTransaction({
        'chainId': 97,
        'gas': gas,
        'gasPrice': gas_price,
        'nonce': nonce,
    })

    signed_txn = w3.eth.account.signTransaction(token_txn, private_key=wallet_key)
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return {"tx_id": tx_receipt.transactionHash.hex()}


async def check_amount_to_send(balance, token_name, gas, request_amount=None, token_decimals=None):
    w3.eth.generate_gas_price(fast_gas_price_strategy)
    gas_price = w3.eth.gasPrice

    if request_amount:
        converted_request_amount = w3.toWei(Decimal(request_amount), 'ether') if token_name == NAITIVE_TOKEN \
            else convert_to_wei(request_amount, token_decimals)

        if converted_request_amount <= int(balance) - gas_price * gas:
            amount_to_send = converted_request_amount
            return amount_to_send, gas_price
        else:
            return "error : not enought balance"
    else:
        if gas_price * gas < int(balance):
            amount_to_send = int(balance) - gas_price * gas
            return amount_to_send, gas_price
        else:
            return "error : not enought balance"
# TODO: replace everywhere "error : not enought balance"

async def create_transaction(request, session=None):

    from_wallet = MAIN_WALLET_ADDRESS if not request.from_wallet or request.from_wallet == MAIN_WALLET_ADDRESS \
        else request.from_wallet
    to_wallet = request.to_address

    wallet_key = MAIN_WALLET_KEY if not request.from_wallet or request.from_wallet == MAIN_WALLET_ADDRESS \
        else await get_wallet_key(session=session, address=request.from_wallet)

    if request.currency.upper() == NAITIVE_TOKEN:
        gas = 21000
        balance = w3.eth.getBalance(from_wallet)

        amount_to_send, gas_price = await check_amount_to_send(balance=balance,
                                                               gas=gas,
                                                               token_name=NAITIVE_TOKEN,
                                                               request_amount=request.amount)

        try:
            tx_id = await create_main_currency_transaction(from_wallet=from_wallet,
                                                           to_wallet=to_wallet,
                                                           gas=gas,
                                                           gas_price=gas_price,
                                                           amount_to_send=amount_to_send,
                                                           wallet_key=wallet_key)
        except ValueError as exc:
            return exc.args

        await add_trans(session=session,
                        from_wallet=from_wallet,
                        to_address=to_wallet,
                        amount=amount_to_send,
                        currency=request.currency.upper(),
                        tx_id=tx_id.get('tx_id'))
        return tx_id
    else:
        gas = 420000
        tokens_balances = await get_tokens_balances(wallet_address=from_wallet)

        currency, token_decimals, balance, contr_addr = tuple(*[(token.get('contract_ticker_symbol'),
                                                                 token.get('contract_decimals'),
                                                                 token.get('balance'),
                                                                 token.get('contract_address'))
                                                                for token in tokens_balances
                                                                if token.get(
                'contract_ticker_symbol') == request.currency.upper()])

        amount_to_send, gas_price = await check_amount_to_send(balance=balance,
                                                               gas=gas,
                                                               token_name=request.currency.upper(),
                                                               request_amount=request.amount,
                                                               token_decimals=token_decimals)

        try:
            tx_id = await create_token_transaction(from_wallet=from_wallet,
                                                   to_wallet=to_wallet,
                                                   gas=gas,
                                                   gas_price=gas_price,
                                                   amount_to_send=amount_to_send,
                                                   wallet_key=wallet_key,
                                                   contr_addr=contr_addr)
        except ValueError as exc:
            return exc.args

        await add_trans(session=session,
                        from_wallet=from_wallet,
                        to_address=to_wallet,
                        amount=amount_to_send,
                        currency=request.currency.upper(),
                        tx_id=tx_id.get('tx_id'))

        return tx_id
