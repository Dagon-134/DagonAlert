import logging

from binance_common.configuration import ConfigurationRestAPI
from binance_common.constants import DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL
from binance_sdk_derivatives_trading_usds_futures.derivatives_trading_usds_futures import DerivativesTradingUsdsFutures
from binance_sdk_derivatives_trading_usds_futures.rest_api.models import ExchangeInformationResponse

config = ConfigurationRestAPI(
    api_key="",
    api_secret="",
    base_path=DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL,
)


client = DerivativesTradingUsdsFutures(
    config_rest_api=config
)

class GetCoins:
    
    def __init__(self, client):
        self.client = client
        
    def get_coins(self):
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
    
    