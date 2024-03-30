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


def call_history(method: Callable) -> Callable:
    """decorator to store the history of inputs
       and outputs for a particular function
    """
    @functools.wraps(method)
    def history_wrapper(self, *args, **kwargs):
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output

    return history_wrapper


def replay(method: Callable) -> None:
    """display the history of calls of @method"""
    __redis_cache = redis.Redis()
    inputs = __redis_cache.lrange(f'{method.__qualname__}:inputs', 0, -1)
    outputs = __redis_cache.lrange(f'{method.__qualname__}:outputs', 0, -1)

    print(f'{method.__qualname__} was called '
          f'{int(__redis_cache.get(method.__qualname__))} times:')
    for inp, out in zip(inputs, outputs):
        print(f'{method.__qualname__}(*{inp.decode("utf-8")}) '
              f'-> {out.decode("utf-8")}')


class Cache:
    """cache class"""

    def __init__(self) -> None:
        """init redis cache"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
