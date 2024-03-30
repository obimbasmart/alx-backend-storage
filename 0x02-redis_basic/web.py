#!/usr/bin/env python3

"""Implementing an expiring web cache and tracker"""

import requests
import redis


r = redis.Redis()


def get_page(url: str) -> str:
    """obtain html content of a web page
        and cache result for 10s
    """
    cached_result = r.get(url)
    if cached_result:
        return cached_result

    response = requests.get(url).text
    r.set(url, response, ex=10)
    return response