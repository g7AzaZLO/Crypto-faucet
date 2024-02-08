import hexbytes.main
from web3 import Web3

RPC_URL = ""
ADMIN_USER_ID =
TG_BOT_KEY = ""
WALLET_ADDR = ""
DATABASE_FILE = "faucet.db"
MNEMONIC = ""
NUM_TOKEN_TO_SEND = 15 # Количество токенов которое необходимо выдавать
CHECK_UNDER_NUM_TOKEN = 11 # Проверка на баланс ниже данного значения

web3 = Web3(Web3.HTTPProvider(RPC_URL))


def get_private() -> hexbytes.main.HexBytes:
    web3.eth.account.enable_unaudited_hdwallet_features()
    account = web3.eth.account.from_mnemonic(MNEMONIC)
    private_key = account._private_key
    return private_key


WALLET_PK = get_private()
