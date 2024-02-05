import asyncio
import sqlite3
from typing import Any, Coroutine
from eth_typing import HexStr
from web3 import Web3
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from settings.config import RPC_URL, ADMIN_USER_ID, DATABASE_FILE, WALLET_ADDR, WALLET_PK
from process.db import delete_user_from_db, execute_non_query
from process.other import ping_admin_dm

router_claim = Router()


# Проверка юзера на использование крана и отсутсвтие баланса
async def check_user(user: int, address: str) -> str:
    if not await is_low_balance(user, address):
        delete_user_from_db(user)
        return "You have enough funds!"
    if not await is_low_balance(user, address):
        delete_user_from_db(user)
        return "You have used the Faucet recently! Wait 24h"
    execute_non_query("INSERT INTO faucetClaims (USER_ID, ADDR, DT) VALUES (" + str(
        user) + ", '" + address + "', julianday(('now')));")
    return await check_tx(await send_token(address, user), address, user)


async def is_low_balance(user: int, address: str) -> bool:
    try:
        web3 = Web3(Web3.HTTPProvider(RPC_URL))
        balance = web3.eth.get_balance(address)
        if user == ADMIN_USER_ID:
            return True
        elif balance < 11:
            return True
        return False
    except Exception as e:
        return True


async def is_not_use(user: int, address: str) -> bool:
    conn = sqlite3.connect(DATABASE_FILE).cursor()
    conn.execute("SELECT 1 FROM faucetClaims WHERE (USER_ID = " + str(
        user) + " OR ADDR = '" + address + "') AND DT > julianday('now', '-24 hours') ")
    rows = conn.fetchall()
    if user == ADMIN_USER_ID:
        return True
    elif (len(rows)) == 0:
        return True
    return False


async def send_token(address: str, user: int) -> HexStr | None:
    try:
        web3 = Web3(Web3.HTTPProvider(RPC_URL))
        nonce = web3.eth.get_transaction_count(WALLET_ADDR)
        tx = {
            'nonce': nonce,
            'to': address,
            'value': web3.to_wei(15, 'ether'),
            'gas': 50000,
            'gasPrice': web3.to_wei('100', 'gwei')}
        signed_tx = web3.eth.account.sign_transaction(tx, WALLET_PK)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print("send")
        return web3.to_hex(tx_hash)
    except Exception as e:
        print(f"ERROR: {e}\nContinue...")
        await ping_admin_dm(f"ERROR: {e}")
        delete_user_from_db(user)
        return None


async def check_tx(tx_hash, address, user) -> str:
    try:
        web3 = Web3(Web3.HTTPProvider(RPC_URL))
        data = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=20)
        if 'status' in data and data['status'] == 1:
            print(f"{address} | transaction was sucsessfull: {tx_hash}")
            return f"Transaction was sucsessfull: {tx_hash}"
        else:
            delete_user_from_db(user)
            print(f"{address} | transaction failed {data['transactionHash'].hex()}")
            return f"Transaction failed {data['transactionHash'].hex()}"
    except Exception as err:
        delete_user_from_db(address)
        print(f"{address} | unexpected error in <check_tx> function: {err}")
        return f"Unexpected error in <check_tx> function: {err}"


# Обработка команды /claim
@router_claim.message(Command('claim'))
async def claim(message: Message):
    user = message.from_user.id
    address = message.text.split(' ')[1]
    result = await check_user(user, address)
    await message.reply(result)
