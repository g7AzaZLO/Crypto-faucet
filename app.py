import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from settings.config import TG_BOT_KEY
from process.other import ping_admin_dm
from process.db import create_db
from process.claim import router_claim

# Инициализация бота
bot = Bot(token=TG_BOT_KEY)
dp = Dispatcher()
dp.include_router(router_claim)

# Команды бота
cmd = [
    BotCommand(command='claim', description='<address>'),
    BotCommand(command='distribution', description='only for admin'),
]


# Запуск бота
async def main() -> None:
    await bot.set_my_commands(commands=cmd)
    await bot.delete_webhook(drop_pending_updates=True)
    print("Start bot")
    await ping_admin_dm("Start bot")
    await create_db()
    await dp.start_polling(bot)


asyncio.run(main())
