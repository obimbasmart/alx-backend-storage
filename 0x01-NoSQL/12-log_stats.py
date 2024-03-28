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
    server_logs_collection = client[db][collection]
    logs = [log for log in server_logs_collection.find({})]
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    grouped_logs = {
        method: len([log for log in logs if log['method'] == method])
        for method in methods
    }
    status_check = len([log for log in logs
                        if log['method'] == "GET" and
                        log['path'] == '/status'
                        ])

    return ('{} logs\nMethods:\n    method GET: {}\n    method POST: {}\n    method '
            'PUT: {}\n    method PATCH: {}\n    method DELETE: {}\n{} status check'
            .format(
                len(logs),
                *grouped_logs.values(), status_check
            ))


if __name__ == "__main__":
    print(nginx_stats('logs', 'nginx'))
