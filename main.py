from aiogram import Bot, Dispatcher

from sql import Repo

from dotenv import load_dotenv
import os

from handlers import rt_handler

from binance_common.configuration import ConfigurationRestAPI
from binance_common.constants import DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL
from binance_sdk_derivatives_trading_usds_futures.derivatives_trading_usds_futures import DerivativesTradingUsdsFutures

config = ConfigurationRestAPI(
    api_key="",
    api_secret="",
    base_path=DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL,
)

from src.domain.get_coins import GetCoins
from handlers import send_alert

import asyncio

load_dotenv()

bot_url = os.getenv("BOT_TOKEN")
if bot_url is None:
    raise ValueError("Переменная окружения BOT_TOKEN не задана!")
bot = Bot(token=bot_url)

dp = Dispatcher()

async def alert_callback(text):
    await send_alert(text, dp['repo'])

async def main():
    client = DerivativesTradingUsdsFutures(
        config_rest_api=config
    )
    connect = os.getenv('TABLE')
    dp['repo'] = Repo(connect)
    print('дошёл')
    get_coins = GetCoins(client)
    print('начал')
    dp.include_router(rt_handler)
    take_task = asyncio.create_task(get_coins.get_coins(on_signal=alert_callback))

    try:
        await dp.start_polling(bot)

    finally:
        take_task.cancel()

        try:
            await take_task
        except asyncio.CancelledError:
            pass

asyncio.run(main())