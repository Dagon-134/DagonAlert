import logging

from binance_sdk_derivatives_trading_usds_futures.rest_api.models import ExchangeInformationResponse

from domain.checking_changes_1m import CheckingCoins_1m
from src.domain.checking_changes_5m import CheckingCoins_5m


class GetCoins:
    
    def __init__(self, client):
        self.client = client
        
    async def get_coins(self):
        print('Начинаю доставать монеты')
        check_1m = CheckingCoins_1m()
        check_5m = CheckingCoins_5m()
        try:
            response = self.client.rest_api.exchange_information()
            
            data: ExchangeInformationResponse = response.data()
            logging.info(f"exchange_information() response: {data}")
            if data.symbols is not None:
                coins = [symbol 
                        for symbol in data.symbols 
                        if symbol.quote_asset == 'USDT'
                        and symbol.status == 'TRADING'
                        and symbol.contract_type == 'PERPETUAL']
            
                await check_5m.checking(coins)
                await check_1m.checking(coins)
            
                
            
        except Exception as e:
            logging.error(f"exchange_information() error: {e}")
    
    