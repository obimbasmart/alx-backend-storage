#!/usr/bin/env python3

"""
function returns a list of all documents in a collection:

    mongo_collection will be the pymongo collection object
"""

from typing import List


def list_all(mongo_collection) -> List[dict]:
    """return list of docs in collection"""
    return [doc for doc in mongo_collection.find({})]
