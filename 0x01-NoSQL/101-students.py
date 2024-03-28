#!/usr/bin/env python3

"""
Write a Python function that returns all students sorted by average score:

    Prototype: def top_students(mongo_collection):
    mongo_collection will be the pymongo collection object
    The top must be ordered
    The average score must be part of each item returns with key = averageScore
"""


def top_students(mongo_collection):
    """get top students"""
    students = [student for student in mongo_collection.find()]
    for student in students:
        average_score = sum([topic["score"]
                             for topic in
                             student["topics"]]) / 3

        mongo_collection.update_one({"_id": student["_id"]},
                                    {
                                        "$set": {"averageScore": average_score}
        })

    return sorted([student for student in mongo_collection.find()],
                  key=lambda x: x['averageScore'], reverse=True)
