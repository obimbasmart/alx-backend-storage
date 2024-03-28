#!/usr/bin/env python3

"""
Improve 12-log_stats.py by adding the top 10 of the most
present IPs in the collection nginx of the database logs:

The IPs top must be sorted (like the example below)
"""

from pymongo import MongoClient


def nginx_stats(db, collection):
    """logs out nginx server logs"""
    client = MongoClient()
    nginx_logs = client[db][collection]
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    print(nginx_logs.count_documents({}), "logs")
    print("Methods:")
    for method in methods:
        count = nginx_logs.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    print(nginx_logs.count_documents({"method": 'GET', 'path': '/status'}),
          'status check')

    print('IPs:')
    result = nginx_logs.aggregate(
        [
            {
                "$group": {
                    "_id": "$ip",
                    "count": {"$sum": 1}
                }
            },

            {
                "$sort": {"count": -1}
            },

            {
                "$limit": 10
            }

        ]
    )

    [print(f'\t{re["_id"]}: {re["count"]}') for re in result]


if __name__ == "__main__":
    nginx_stats('logs', 'nginx')
