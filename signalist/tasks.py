from rest_framework import status

from signal_producer.adapters.redis_adapter import RedisAdapter
from signalist.utils.binance_api_utils import BinanceAPIUtils


def producer_task(currency_name: str):
    # request to Binance API to get data
    data = BinanceAPIUtils.get_currency_pair_data_from_binance(currency_name=currency_name)

    if data.status != status.HTTP_200_OK:
        # log here
        print("Binance API failed!")
        return

    currency_price = data[-1]
    timestamp = data[-1][0]

    RedisAdapter().set_currency_timestamp_price_redis_cache(
        currency_name=currency_name,
        timestamp=timestamp,
        currency_price=currency_price)
