#!/usr/bin/env python3

"""Redis cache implementtion"""

import redis
import uuid
from typing import Union, Callable, Any
import functools


def count_calls(method: Callable) -> Callable:
    """decorator - count the number of times a func is called"""
    @functools.wraps(method)
    def count_wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return count_wrapper


class Cache:
    """cache class"""

    def __init__(self) -> None:
        """init redis cache"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store the input data in Redis"""
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Union[Callable[[bytes], Any], None] = None) -> Any:
        """get data from redis and convert to desired format"""
        data: bytes = self._redis.get(key)
        if data and fn is not None:
            return fn(data)
        return data

    def get_str(self, data: bytes) -> str:
        """convert to str"""
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """convert to integer"""
        return int(data)
