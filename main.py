from aiogram import Bot, Dispatcher

from sql import Repo

import logging

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
from src.domain.checking_changes_1m import CheckingCoins_1m
from src.domain.checking_changes_5m import CheckingCoins_5m
from src.domain.get_top_high_low_coins_24h import TopHighLow
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
    logging.basicConfig(level=logging.INFO)
    ##
    client = DerivativesTradingUsdsFutures(
        config_rest_api=config
    )
    logging.info([name for name in dir(client.rest_api) if "ticker" in name.lower()])
    ##
    connect = os.getenv('TABLE')
    dp['repo'] = Repo(connect)
    logging.info(f'Подключение к дб:{connect}')
    ##
    logging.info('ДОШЁЛ')
    ##
    get_coins = GetCoins(client)
    dp['top'] = TopHighLow(client)
    coins = await get_coins.get_coins()
    ##
    check_1m = CheckingCoins_1m()
    check_5m = CheckingCoins_5m()
    ##
    dp.include_router(rt_handler)
    ##
    logging.info('Начинаю просмотр всех монет')
    take_task = asyncio.gather(
        check_5m.checking(coins, on_signal=alert_callback),
        check_1m.checking(coins, on_signal=alert_callback))

    try:
        await dp.start_polling(bot)

    finally:
        take_task.cancel()

        try:
            await take_task
        except asyncio.CancelledError:
            pass

asyncio.run(main())