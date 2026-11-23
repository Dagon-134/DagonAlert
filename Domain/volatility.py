import asyncio
import time

from binance import AsyncClient

class Volatility:
    
    def __init__(self, client):
        self.client = client
        self.semaphore = asyncio.Semaphore(5)
    
    
    async def calculate_atr(self, klines, period=14):

        if len(klines) < period + 1:
            return None

        true_ranges = []

        for i in range(1, len(klines)):

            high = float(klines[i][2])
            low = float(klines[i][3])
            prev_close = float(klines[i - 1][4])

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )

            true_ranges.append(tr)

        if len(true_ranges) < period:
            return None

        # Первоначальный ATR
        atr = sum(true_ranges[:period]) / period

        # Сглаживание Уайлдера до последнего значения
        for tr in true_ranges[period:]:
            atr = (
                atr * (period - 1) + tr
            ) / period

        return atr
        
    
    async def get_high_atr(self, symbol_m):
        
        async with self.semaphore:
            try:
                klines = await self.client.futures_klines(
                    symbol=symbol_m,
                    interval=AsyncClient.KLINE_INTERVAL_15MINUTE,
                    limit=50
                )
                
                now = int(time.time() * 1000)
                
                closed_klines = [
                    k
                    for k in klines
                    if int(k[6]) < now
                ]
                
                if len(closed_klines) < 15:
                    return None
                
                atr = await self.calculate_atr(closed_klines, period=14)
                
                close_price = float(closed_klines[-1][4])
                
                if close_price is None:
                    return None
                
                if atr is None:
                    return None
                
                
                atr_percent = (atr / close_price) * 100
                
                return {
                    "symbol": symbol_m,
                    "atr": atr,
                    "atr_percent": round(atr_percent, 2),
                    "price": close_price
                }
                
                
            except Exception as e:
                print(e)
    
    async def get_top_volatility(self, limit=10):
        print('Начинаю волатилить')
        exchange_info = await self.client.futures_exchange_info()
        
        symbols = [
            symbol['symbol'] 
            for symbol in exchange_info["symbols"]
            if symbol["quoteAsset"] == "USDT"
            and symbol['status'] == 'TRADING'
            and symbol['contractType'] == 'PERPETUAL']
        
        results = await asyncio.gather(
            *[
                self.get_high_atr(symbol)
                for symbol in symbols
            ]
        )
        
        results = [result 
                    for result in results 
                    if result != None]
        
        results.sort(
            key=lambda x: x["atr_percent"],
            reverse=True
        )
        print('выполнил')

        return results[:limit]