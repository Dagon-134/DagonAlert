import logging
import json

from binance_sdk_derivatives_trading_usds_futures.rest_api.models import ExchangeInformationResponse


class GetCoins:
    
    def __init__(self, client):
        self.client = client
        
    async def get_coins(self):
        logging.info('достаю монеты')
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

                return coins
            
                
            
        except Exception as e:
            logging.error(f"exchange_information() error: {e}")
    
    