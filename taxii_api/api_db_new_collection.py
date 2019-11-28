from pymongo import MongoClient
import bson
import uuid

# connect to  Mongo database
connection = MongoClient('localhost', 27018)
api_name = 'demo_api'
db = connection[api_name]


collections_doc = {
        "id": str(uuid.uuid4()),
        "title": "Second TAXII Demo Collection",
        "description": "This data collection contains STIX 2.0 objects related to threat reports which are about threats targeting private organizations, companies, financial organizations or IT security companies.It is for demonstrating purposes too.",
        "can_read": True,
        "can_write": True,
        "media_types": [
          "application/vnd.oasis.stix+json; version=2.0"
        ]
      }

collection1_bson = db.collections.insert_one(collections_doc)
