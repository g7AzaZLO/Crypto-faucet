import hexbytes.main
from web3 import Web3

RPC_URL = ""  # RPC сети в которой будут выдаваться токены
ADMIN_USER_ID =   # Телеграм ID юзера, который будет считаться админов(можно выдавать токены кому угодно и
# сколько хочешь раз)
TG_BOT_KEY = "" # Телеграм токен от бота
WALLET_ADDR = "" # Адрес кошелька с которого будут выдаваться токены
DATABASE_FILE = "faucet.db" # Название файла с базой
MNEMONIC = "" # Мнемоника от кошелька крана
NUM_TOKEN_TO_SEND = 15  # Количество токенов которое необходимо выдавать
CHECK_UNDER_NUM_TOKEN = 11  # Проверка на баланс ниже данного значения

web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Конвертация мнемоники в приватный ключ
def get_private() -> hexbytes.main.HexBytes:
    web3.eth.account.enable_unaudited_hdwallet_features()
    account = web3.eth.account.from_mnemonic(MNEMONIC)
    private_key = account._private_key
    return private_key


WALLET_PK = get_private() # Вместо использования мнемоники можно напрямую вставить приватный ключ сюда
