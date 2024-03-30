#!/usr/bin/env python3

"""Implementing an expiring web cache and tracker"""

import requests
import redis
from typing import Callable
import functools


__redis = redis.Redis()


def cache_request(method: Callable) -> Callable:
    """cache decorator: track ntimes func is called
       and cache result for 10s"""
    @functools.wraps(method)
    def cache_wrapper(url):
        __redis.incr(f'count:{url}')
        cached_result = __redis.get(f'cached:{url}')
        if cached_result:
            return cached_result.decode('utf-8')

        response = method(url)
        __redis.setex(f'cached:{url}', 10, response)
        return response

    return cache_wrapper


@cache_request
def get_page(url: str) -> str:
    """obtain html content of a web page
    """
    return requests.get(url).text
