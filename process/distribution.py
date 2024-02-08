import asyncio
from typing import Any
from web3 import Web3
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from settings.config import RPC_URL, WALLET_ADDR, WALLET_PK, NUM_TOKEN_TO_SEND

router_distribution = Router()


async def string_to_address_list(text: str) -> list[str]:
    address_list = text.split('\n')[
                   1:]  # разделяем строку по символу переноса строки и пропускаем первый элемент
    return address_list


async def send_token(address: str) -> Any | None:
    try:
        print("new query")
        web3 = Web3(Web3.HTTPProvider(RPC_URL))
        nonce = web3.eth.get_transaction_count(WALLET_ADDR)
        tx = {
            'nonce': nonce,
            'to': address,
            'value': web3.to_wei(NUM_TOKEN_TO_SEND, 'ether'),
            'gas': 6000000,
            'gasPrice': web3.to_wei('2000', 'gwei')}

        signed_tx = web3.eth.account.sign_transaction(tx, WALLET_PK)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print("send")
        return web3.to_hex(tx_hash)
    except Exception as e:
        print(f"ERROR: {e}\nContinue...")
        return None


async def check_tx(tx_hash, address) -> bool:
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    try:
        data = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=20)
        if 'status' in data and data['status'] == 1:
            print(f"{address} | transaction was sucsessfull: {tx_hash}")
            return True
        else:
            print(f"{address} | transaction failed {data['transactionHash'].hex()}")
            return False
    except Exception as err:
        print(f"{address} | unexpected error in <check_tx> function: {err}")
        return False


@router_distribution.message(Command('distribution'))
async def contribute(message: Message):
    address = await string_to_address_list(message.text)
    while True:
        new_addr_list = []
        for i in address:
            if not await check_tx(await send_token(i), i):
                new_addr_list.append(i)
            else:
                continue
        print(new_addr_list)
        address = new_addr_list
        if len(new_addr_list) == 0:
            break
