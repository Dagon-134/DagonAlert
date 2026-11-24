import asyncio
import websockets
import json

async def checking():
    async with websockets.connect('wss://fstream.binance.com/market/ws/btcusdt@kline_1m') as ws:
        async for message in ws:
            message = json.loads(message)
            if message["k"]["x"] == True:
                res = ((float(message["k"]["c"]) - float(message["k"]["o"])) / float(message["k"]["c"])) * 100
                print(f'монета {message['s']} изменила цену на {res:.2f}%')
            
asyncio.run(checking())