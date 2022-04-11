from typing import List, Optional

import redis
from decouple import config

from signal_producer.config.redis_key_config import RedisKeysConfig


class RedisAdapter:

    def __init__(self,
                 host=config('REDIS_1_HOST_IP'),
                 port=config('REDIS_1_HOST_PORT'),
                 db=config('REDIS_1_DB'),
                 password=config('REDIS_1_PASSWORD')):
        self.redis_obj = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password)

    def set_currency_pair_list_redis_cache(self, new_currency_name: str) -> None:
        cache_value = self.get_currency_pair_list_redis_cache()

        if cache_value:
            cache_value += new_currency_name + ","

        else:
            cache_value = new_currency_name + ","

        self.redis_obj.set(
            name=RedisKeysConfig.CurrencyPairList.key_template,
            value=cache_value,
            ex=RedisKeysConfig.CurrencyPairList.ttl_time)

    def get_currency_pair_list_redis_cache(self) -> Optional[List]:
        key = RedisKeysConfig.CurrencyPairList.key_template
        value = self.redis_obj.get(name=key)

        if value:
            value = value.decode('utf-8').split(',')[:-1]

        return value

    def set_currency_timestamp_price_redis_cache(self, currency_name: str, timestamp: int,
                                                 currency_price: float) -> None:
        self.redis_obj.set(
            name=RedisKeysConfig.CurrencyTimestampData.key_template.format(
                currency_name=currency_name,
                timestamp=timestamp),
            value=currency_price,
            ex=RedisKeysConfig.CurrencyTimestampData.ttl_time)

    def get_currency_timestamp_price_redis_cache(self, currency_name: str, timestamp: int) -> float:
        key = RedisKeysConfig.CurrencyTimestampData.key_template.format(
            currency_name=currency_name,
            timestamp=timestamp)

        return float(self.redis_obj.get(name=key).decode('utf-8'))
