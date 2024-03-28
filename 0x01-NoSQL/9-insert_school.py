#!/usr/bin/env python3

"""Insert a document into mongodb collection"""


def insert_school(mongo_collections, **kwargs):
    """insert doc"""
    return mongo_collections.insert_one(kwargs).inserted_id
