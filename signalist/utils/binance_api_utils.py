from typing import Dict

import requests

from signal_producer.constants.base_constants import BaseConstants


class BinanceAPIUtils:
    binance_api_url = url = 'https://api.binance.com/api/v3/klines'

    @classmethod
    def get_currency_pair_data_from_binance(cls, currency_name: str, tick_interval: str = '1m'):
        query_params: Dict[str, str] = {
            BaseConstants.symbol: currency_name,
            BaseConstants.interval: tick_interval,
        }

        response = requests.get(cls.binance_api_url, params=query_params)

        return response.json()
