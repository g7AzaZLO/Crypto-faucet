import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from settings.config import TG_BOT_KEY

# Инициализация бота
bot = Bot(token=TG_BOT_KEY)
dp = Dispatcher()

# Команды бота
cmd = [
    BotCommand(command='claim', description='<address>'),
    BotCommand(command='distribution', description='only for admin'),
]


# Запуск бота
async def main() -> None:
    await bot.set_my_commands(commands=cmd)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
