import websockets
import json

import logging

class TopHighLow:
    
    def __init__(self, client):
        self.client = client
        
    def get_top(self):
        response = self.client.rest_api.ticker24hr_price_change_statistics()
        rate_limits = response.rate_limits
        data = response.data()
        
        tickers = data.actual_instance

        # Сортируем по проценту изменения цены (по убыванию)
        top_growth = sorted(
            tickers, 
            key=lambda x: float(x.price_change_percent), 
            reverse=True
        )
        top_fall = sorted(
            tickers, 
            key=lambda x: float(x.price_change_percent), 
        )
        
        answer_high = []
        answer_low = []

        for ticker in top_growth[:10]:
            answer_high.append(f"{ticker.symbol} || {ticker.price_change_percent}%")
            
        for ticker in top_fall[:10]:
            answer_low.append(f"{ticker.symbol} || {ticker.price_change_percent}%")
            
        return f'ТОП 10 роста и падения:\n{'\n'.join(answer_high)}\n____{'\n'.join(answer_low[::-1])}'