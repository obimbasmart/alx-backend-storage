#!/usr/bin/env python3

"""
function that returns the list of school having a specific topic:

    Prototype: def schools_by_topic(mongo_collection, topic):
    mongo_collection will be the pymongo collection object
    topic (string) will be topic searched

"""


def schools_by_topic(mongo_collection, topic):
    """get schools by topic"""
    result = mongo_collection.find({"topics": {"$in": [topic]}})
    return [school for school in result]
