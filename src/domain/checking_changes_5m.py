import websockets
import json
import logging

PERCENT_FOR_ALERT = 5.0

class CheckingCoins_5m:
    
    def chunks(self, list, size=100):
        for i in range(0, len(list), size):
            yield list[i:i + size]
    
    async def checking(self, coins, on_signal):
        
        async with websockets.connect('wss://fstream.binance.com/market/stream') as ws:
            subscribe_message = {"method": "SUBSCRIBE", "params": [], "id": 1}
            coins_names = []
            logging.info('прохожусь по списку')
            for coin in coins:
                coins_names.append(str.lower(coin.symbol) + '@kline_5m')
                
            logging.info('Прошёлся по списку')
            coins_names = list(self.chunks(coins_names))
            for number, chunk in enumerate(coins_names, start=1):
                subscribe_message["id"] = number
                subscribe_message["params"] = chunk
                message = json.dumps(subscribe_message)
                print(len(coins_names))
                await ws.send(message)
            print('отправил')
            async for message in ws:
                message = json.loads(message)
                if "data" not in message or "k" not in message["data"]:
                    continue
                if message["data"]["k"]["x"] is True:
                    close_price = float(message["data"]["k"]["c"])
                    open_price = float(message["data"]["k"]["o"])
                    res = ((close_price - open_price) / open_price) * 100
                    
                    if res >= PERCENT_FOR_ALERT:
                        print(f"🚨🚨🚨\n{message["data"]["s"]} выросла на {res:.2f}% за 5 минут\n🚨🚨🚨")
                        signal = f"🚨🚨🚨\n{message["data"]["s"]} выросла на {res:.2f}% за 5 минут\n📈Цена: {message['data']['k']['c']}\n🚨🚨🚨"
                        await on_signal(signal)
                        
                    elif res <= -PERCENT_FOR_ALERT:
                        print(f"🚨🚨🚨\n{message["data"]["s"]} упала на {res:.2f}% за 5 минут\n🚨🚨🚨")
                        signal = f"🚨🚨🚨\n{message["data"]["s"]} упала на {res:.2f}% за 5 минут\n📉Цена: {message['data']['k']['c']}\n🚨🚨🚨"
                        await on_signal(signal)