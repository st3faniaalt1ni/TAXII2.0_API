from pymongo import MongoClient
import bson
import uuid

# connect to database
connection = MongoClient('localhost', 27018)

discovery_db = {"title": "Demonstration TAXII Server",
     "description": "This TAXII Server contains a APT1 example dataset",
     "contact": "Stefania Altini",
     "default": "http://localhost:5000/demo_api/",
     "api_roots": [
         "demo_api"
     ]}

db = connection['discovery_database']
db_bson = db.discovery_information.insert_one(discovery_db)
api_name = 'demo_api'
api_description = {
    "title": "Demonstrative API",
    "description": "A demo api for my thesis",
    "versions": [
          "taxii-2.0"
    ],
    "max_content_length": 9765625,
    "_url": "http://localhost:5000/demo_api/",
    "_name": "demo_api"
    }

api_info_bson = db.api_root_info.insert_one(api_description)


collections_doc = {
        "id": str(uuid.uuid4()),
        "title": "Demo Collection",
        "description": "This data collection is for demonstrating purposes",
        "can_read": True,
        "can_write": True,
        "media_types": [
          "application/vnd.oasis.stix+json; version=2.0"
        ]
      }


db = connection[api_name]
collection1_bson = db.collections.insert_one(collections_doc)
