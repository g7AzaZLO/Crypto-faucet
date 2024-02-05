import asyncio
from aiogram import Bot
from settings.config import TG_BOT_KEY, ADMIN_USER_ID

bot = Bot(token=TG_BOT_KEY)


# Отправка сообщения админу
async def ping_admin_dm(msg: str) -> None:
    print("ping admin: " + msg)
    await bot.send_message(ADMIN_USER_ID, msg)
