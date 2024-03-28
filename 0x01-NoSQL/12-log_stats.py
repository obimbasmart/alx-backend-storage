#!/usr/bin/env python3

"""
script that provides some stats about Nginx logs stored in MongoDB:

Database: logs
Collection: nginx
Display (same as the example):
"""

from pymongo import MongoClient

client = MongoClient()
server_logs_collection = client.logs.nginx
logs = [log for log in server_logs_collection.find({})]

methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

grouped_logs = {
    method: len([log for log in logs if log['method'] == method])
    for method in methods
}

print('{} logs\nMethods:\n\tmethod GET {}\n\tmethod POST {}\n\tmethod '
      'PUT {}\n\tmethod PATCH {}\n\tmethod DELETE {}'.format(
          len(logs),
          *grouped_logs.values()
      ))
