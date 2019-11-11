from pymongo import MongoClient
import bson
import uuid

# connect to database
connection = MongoClient('localhost', 27018)
api_name = 'demo_api'
db = connection[api_name]


collections_doc = {
        "id": str(uuid.uuid4()),
        "title": "Second Demo Collection",
        "description": "This data collection contains  STIX 2.0 objects  related to indicators  which contain a pattern that can be used to detect suspicious or malicious cyber activity.This collection is also  for demonstrative purposes",
        "can_read": True,
        "can_write": True,
        "media_types": [
          "application/vnd.oasis.stix+json; version=2.0"
        ]
      }

collection1_bson = db.collections.insert_one(collections_doc)
