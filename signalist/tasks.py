import datetime
import time
from typing import Dict, Any

import requests
from rest_framework import status

from signal_producer.adapters.redis_adapter import RedisAdapter
from signal_producer.constants.base_constants import BaseConstants
from signal_producer.constants.channel_addresses_constants import channel_addresses_constants
from signal_producer.signalist_celery import app
from signalist.utils.binance_api_utils import BinanceAPIUtils


@app.task(bind=True)
def producer_task(self, currency_name: str):
    # request to Binance API to get data
    data = BinanceAPIUtils.get_currency_pair_data_from_binance(currency_name=currency_name)

    if data.status_code != status.HTTP_200_OK:
        # log here
        print("Binance API failed!")
        return

    data = data.json()

    currency_price = float(data[-1][4])  # Close Price
    timestamp = int(str(data[-1][6])[:-3])  # Close timestamp in ms

    RedisAdapter().set_currency_timestamp_price_redis_cache(
        currency_name=currency_name,
        timestamp=timestamp,
        currency_price=currency_price)


@app.task(bind=True)
def signaler_task(self, currency_name: str, return_channel_name: str, desired_price: float):
    desired_price = float(desired_price)

    timestamp = int(datetime.datetime.now().replace(minute=datetime.datetime.now().minute - 1, second=59).timestamp())
    currency_actual_price = RedisAdapter().get_currency_timestamp_price_redis_cache(
        currency_name=currency_name,
        timestamp=timestamp)

    while not currency_actual_price:
        # We should try to get data from redis
        time.sleep(secs=10)
        currency_actual_price = RedisAdapter().get_currency_timestamp_price_redis_cache(
            currency_name=currency_name,
            timestamp=timestamp)

    channel_address = channel_addresses_constants.get(return_channel_name)
    request_body: Dict[str, Any] = {
        BaseConstants.timestamp: timestamp,
        BaseConstants.price_range: "up" if currency_actual_price > desired_price else "down",
    }

    requests.post(url=channel_address, data=request_body)
