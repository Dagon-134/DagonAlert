from binance import AsyncClient, BinanceSocketManager 

from aiogram.exceptions import TelegramForbiddenError

import asyncio

from sql import Repo

from handlers import send_alert

ALERT_THRESHOLD = 2.0

class Changes:
    
    async def take(self, group, list):
        client = await AsyncClient.create()
        
        try:
            bm = BinanceSocketManager(client, max_queue_size=2000)
            
            socket = bm.futures_multiplex_socket(group)
            if socket is None: 
                pass
            
            async with socket as stream:
                while True:
                    try:
                        msg = await stream.recv()
                        
                        data = msg['data'] if 'data' in msg else msg
                        if 'k' not in data:
                            continue
                        candle = data['k']
                        
                        if candle['x']:
                            open_price = float(candle['o'])
                            close_price = float(candle['c'])
                            
                            change_percent = ((close_price - open_price) / open_price) * 100
                            
                            if abs(change_percent) >= ALERT_THRESHOLD:
                                try:
                                    if change_percent > 0:
                                        answer = (f"🚨 {data['s']} на +{change_percent:.2f}% за минуту!\n📈Цена: {close_price}")
                                    else:
                                        answer = (f"🚨 {data['s']} на {change_percent:.2f}% за минуту!\n📉Цена: {close_price}")
                                    for id in list:
                                        await send_alert(id, answer)
                                except TelegramForbiddenError:
                                    pass
                    except Exception as e:
                        answer = '👀Что-то пошло не так, перезагрузите бота.\n\n❕Если ничего не заработает обратитесь в поддержку❕'
                        print(f'Ошибка:{e}')
                        for id in list:
                            await send_alert(id, answer)
                                
        finally:
            await client.close_connection()
            
    
    def chunks(self, list, size=100):
        for i in range(0, len(list), size):
            yield list[i:i + size]
            
            
    async def create_groups(self, repo: Repo):
            client = await AsyncClient.create()
            print('дошёл')
            list_of_id = repo.getTgId()
            print(list_of_id)
            while True:
                try:
                    exchange_info = await client.futures_exchange_info()
                    symbols = [s['symbol'] for s in exchange_info['symbols'] if s['symbol'].endswith('USDT') and s['status'] == 'TRADING']
                    
                    streams = [f"{s.lower()}@kline_1m" for s in symbols]
                    
                    groups = list(self.chunks(streams, 100))
                    
                    for group in groups:
                        asyncio.create_task(self.take(group, list_of_id))
                finally:
                    await client.close_connection()