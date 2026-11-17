from binance import AsyncClient, BinanceSocketManager 

ALERT_THRESHOLD = 5.0

class Changes:
    
    async def take(self) -> str:
        client = await AsyncClient.create()
        bm = BinanceSocketManager(client)
        
        exchange_info = await client.futures_exchange_info()
        symbols = [s['symbol'] for s in exchange_info['symbols'] if s['symbol'].enwith('USDT') and s['status'] == 'TRADING']
        
        streams = [f"{s.lower()}@kline_1m" for s in symbols]
        
        socket = bm.futures_multiplex_socket(streams)
        
        async with socket as stream:
            while True:
                msg = await stream.recv()
                
                data = msg['data'] if 'data' in msg else msg
                candle = data['k']
                
                if candle['x']:
                    open_price = float(candle['o'])
                    close_price = float(candle['c'])
                    
                    change_percent = ((close_price - open_price) / open_price) * 100
                    
                    if abs(change_percent) >= ALERT_THRESHOLD:
                        return f"🚨 {data['s']} на {change_percent:.2f}% за минуту! Цена: {close_price}"
                    
        