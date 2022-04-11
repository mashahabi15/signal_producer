from enum import unique, Enum


@unique
class RedisKeysConfig(Enum):
    CurrencyPairList = ("currency_pair_list", None)
    CurrencyTimestampData = ("currency_name:{currency_name}:timestamp:{timestamp}", None)

    def __init__(self, key_format: str, ttl_time: int):
        self.key_template = key_format
        self.ttl_time = ttl_time
