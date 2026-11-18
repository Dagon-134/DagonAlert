from aiogram import Bot, Dispatcher

from sql import Repo

from Domain.take_changes import Changes

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
    ch = Changes()
    dp.include_router(rt_handler)
    take_task = asyncio.create_task(ch.create_groups())

    try:
        await dp.start_polling(bot)

    finally:
        take_task.cancel()

        try:
            await take_task
        except asyncio.CancelledError:
            pass

asyncio.run(main())