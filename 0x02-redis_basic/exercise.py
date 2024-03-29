#!/usr/bin/env python3

"""Redis cache implementtion"""

import redis
import uuid
from typing import Union


class Cache:
    """cache class"""

    def __init__(self) -> None:
        """init redis cache"""

        self.__redis = redis.Redis()
        self.__redis.flushdb()

    def store(self, data: Union[int, float, bytes, str]) -> str:
        """store the input data in Redis"""
        key = str(uuid.uuid1())
        self.__redis.set(key, data)
        return key
