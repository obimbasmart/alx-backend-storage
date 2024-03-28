#!/usr/bin/env python3

"""
script that provides some stats about Nginx logs stored in MongoDB:

Database: logs
Collection: nginx
Display (same as the example):
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


if __name__ == "__main__":
    nginx_stats('logs', 'nginx')
