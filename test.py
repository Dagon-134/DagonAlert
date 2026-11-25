import asyncio
import websockets

async def test():
    async with websockets.connect(
        'wss://fstream.binance.com/market/ws/btcusdt@kline_1m'
    ) as ws:
        async for message in ws:
            print(message)

asyncio.run(test())