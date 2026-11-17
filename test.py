import asyncio
from binance import AsyncClient, BinanceSocketManager

# --- НАСТРОЙКИ ---
SYMBOL = 'BTCUSDT'  # За какой монетой следим
INTERVAL = '1m'     # Интервал свечи (1m = 1 минута)

async def main():
    print("Подключение к Binance...")
    
    # 1. Создаем клиент (ключи не нужны для чтения цен)
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)

    # 2. Открываем поток свечей
    async with bm.kline_socket(symbol=SYMBOL, interval=INTERVAL) as stream:
        print(f"Успешно подключено! Следим за {SYMBOL}. Ждем закрытия свечи...")
        
        while True:
            # 3. Ждем новое сообщение
            msg = await stream.recv()
            
            # Данные о свече лежат внутри ключа 'k'
            candle = msg['k']
            
            # 4. Проверяем, закрылась ли свеча (x == True)
            if candle['x']:
                close_price = candle['c'] # Цена закрытия
                
                # Выводим в консоль
                print(f"🔔 Свеча {INTERVAL} закрылась! Цена {SYMBOL}: {close_price}")
                
                # ========================================================
                # СЮДА ВЫ ПОЗЖЕ ВСТАВИТЕ КОД ОТПРАВКИ В ТЕЛЕГРАМ:
                # await bot.send_message(chat_id=ВАШ_ID, text=f"Цена {SYMBOL}: {close_price}")
                # ========================================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nБот остановлен.")