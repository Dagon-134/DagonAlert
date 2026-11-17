from aiogram import Bot, Dispatcher

from sql import Repo

from dotenv import load_dotenv
import os

from handlers import rt_handler

import asyncio

load_dotenv()

bot_url = os.getenv("BOT_TOKEN")
if bot_url is None:
    raise ValueError("Переменная окружения BOT_TOKEN не задана!")
bot = Bot(token=bot_url)

dp = Dispatcher()

async def main():
    dp['repo'] = Repo()
    dp.include_router(rt_handler)
    await dp.start_polling(bot)

asyncio.run(main())