from app import app, mongo_demo,mongo0
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
import uuid
from datetime import datetime
from stix2validator import validate_instance, print_results


# Endpoints are created according to taxi2 specification
# https://docs.google.com/document/d/1Jv9ICjUNZrOnwUXtenB1QcnBLO35RnjQcJLsa1mGSkI/pub#h.on5bbeus95hi

# On this function, uri's from app.py are connected with the databases names. It must be configured manually in case
# of a new api
def server_db(str):
    map = {
        "discovery_database": mongo0,
        "demo_api": mongo_demo
    }
    return map[str]

@app.route('/taxii/', methods=['GET'])
# returns discovery information for this taxi server
def taxi_discovery():
    database = mongo0.db
    for s in database.discovery_information.find():
        s.pop('_id')
        # documents = mongo.db.collection_name.find()
        resp = dumps(s)
    return resp

# get api info
@app.route('/<api>/', methods=['GET'])
# returns information about demo_api from mongo collection 'api_root_info'
def demo_api_discovery(api):
    # TODO api find in mongo collection discovery_database.api_root_info
    api_name = api
    database = mongo0.db
    # document.name : api_name
    d = database.api_root_info.find_one({"name":api_name})
    if d is not None:
        d.pop('_id')
        resp = dumps(d)
        return resp
    else:
        return not_found()


# function of API to return all taxi collections of specified API (mongo collection 'collections' of API db).
@app.route('/<api>/collections')
def documents(api):
    api_name = api
    database = mongo0.db
    # document.name : api_name
    d = database.api_root_info.find_one({"name": api_name})
    # Check if the api given exists
    if d is not None:
        # Return all documents found in the 'collections' collection
        collections = []
        database = mongo_demo.db
        for col in database.collections.find():
            col.pop('_id')
            collections.append(col)
        if not collections:
            return not_found()
        else:
            resp = dumps(collections)
            return resp
    else:
        return not_found()

# function of API to return a specific taxi collection of specified API (mongo collection 'collections' of API db).
@app.route('/<api>/collections/<id>')
def get_collection_by_id(api,id):
    collection_id = id
    api_name = api
    database = mongo0.db
    # document.name : api_name
    d = database.api_root_info.find_one({"name": api_name})
    # Check if the api given exists
    if d is not None:
        # Return all documents found in the 'collections' collection
        collections = []
        database = mongo_demo.db
        for col in database.collections.find_one({"id": collection_id}):
            col.pop('_id')
            collections.append(col)
        if not collections:
            return not_found()
        else:
            resp = dumps(collections)
            return resp
    else:
        return not_found()

# TODO create manifest creation function
# TODO Create request process function which analyzes bundle and sets status
# TODO connect neo4j instance
# TODO neo4j get collections object function
# TODO get api collections (mongo querie)

def bundle_analysis(db, bundle, collection_id):
    if bundle['type'] == 'bundle':
        status = {
            "id": str(uuid.uuid4()),
            "status": None,
            "request_timestamp": datetime.utcnow(),
            "total_count": len(bundle['objects']),
            "success_count": 0,
            "successes": [],
            "failure_count": 0,
            "failures": [],
            "pending_count": 0,
            "pendings": []
        }
        for object in bundle['objects']:
            results = validate_instance(object)
            if results.is_valid:
                date_added = datetime.utcnow()
                print(object["id"])
                manifest = {
                    "id": object["id"],
                    "date_added": date_added,
                    "versions": [],
                    "media_types": [
                        "application/vnd.oasis.stix+json; version=2.0"
                    ],
                    "_collection_id": collection_id
                }
                manifest['versions'].append(date_added)
                # TODO check if object exists and update manifest instead of adding new
                db.manifest.insert_one(manifest)
                status["success_count"] += 1
                status["successes"].append(object["id"])
                # insert collection_id field and insert object in database
                object['_collection_id'] = collection_id
                db.objects.insert_one(object)
            else:
                status["failure_count"] += 1
                status["failures"].append(object["id"])
        status["status"]='complete'
        db.status.insert_one(status)
        status.pop('_id')
        resp = jsonify(status)
        resp.status_code = 200
        return resp
    else:
        # Respond that submitted input is not a STIX2 bundle
        debugstr = "Submitted Input is not a valid STIX bundle"
        message = {
            'status': 422,
            'message': debugstr,
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp



# Push objects (POST) through route
# <api-root>/collections/<id>/objects/
# or retrieve objects (GET)
# For example
# http://localhost/malicious_URL/add..
@app.route('/<api>/collections/<cid>/objects', methods=['GET','POST'])
# Create a method to push documents into mongo through our api
def get_post_objects_in_collection(api,cid):
    _json = request.json
    _type = _json['type']
    # initially verify api and collection id
    collection_id = cid
    api_name = api
    database = mongo0.db
    # document.name : api_name
    d = database.api_root_info.find_one({"name": api_name})
    # Check if the api given exists
    if d is not None:
        # Use api root db
        database = mongo_demo.db
        # Check if method is POST or GET
        collection_exists = database.collections.find_one({"id": collection_id})
        if collection_exists is not None:
            if request.method == 'POST':
                # In case method is a post, respond with a status object
                # Additionally check that submitted object is a bundle, else return failure
                return bundle_analysis(database, _json, cid)
            else:
                if request.method == 'GET':
                    # Prepare the bundle which will be returned to user with all the values of the collection
                    bundle = {
                        "type": "bundle",
                        "id": "bundle--" + str(uuid.uuid4()),
                        "spec_version": "2.0",
                        "objects": []
                    }
                    for obj in database.objects.find_many({"collection_id": cid}):
                        obj.pop('_id')
                        bundle["objects"].append(obj)
                    resp = dumps(bundle)
                    return resp

        else:
            return not_found()

    else:
        return not_found()





# function of API to find a document with a specific ID
# @app.route('/demo_api/collections/<id>')
# def list_collection(id):
#     document = mongo.db.threats.find_one({'_id': ObjectId(id)})
#     # document = mongo.db.collection_name.find_one({'_id': ObjectId(id)})
#     resp = dumps(document)
#     return resp

# @app.route('/demo_api/collections/<id>/objects')
# def objects(id):
#     document = mongo.db.threats.find_one({'_id': ObjectId(id)})
#     # document = mongo.db.collection_name.find_one({'_id': ObjectId(id)})
#     resp = dumps(document)
#     return resp

# @app.route('/demo_api/collections/<id>/manifest')
# def manifest(id):
#     document = mongo.db.manifest.find_one({'_id': ObjectId(id)})
#     # document = mongo.db.collection_name.find_one({'_id': ObjectId(id)})
#     resp = dumps(document)
#     return resp

# @app.route('/demo_api/collections/<id>/objects/<oid>')
# def object(id):
#     document = mongo.db.threats.find_one({'_id': ObjectId(id)})
#     # document = mongo.db.collection_name.find_one({'_id': ObjectId(id)})
#     resp = dumps(document)
#     return resp

# @app.route('/demo_api/collections/<id>', methods=['PUT', 'PATCH'])
# def update_document(id):
#     _json = request.json
#     # if '$oid' in _json['_id']:
#     # 	id = _json['_id']
#     # 	_id = ObjectId(id['$oid'])
#     # else:
#     # 	_id = ObjectId(_json['_id'])
#     _id = ObjectId(id)
#     # _id = ObjectId(_json['_id'])
#     # _id = ObjectId('5d73abea93f48a8399d3ade6')
#     # _description = _json["description"]
#     # validate the received values
#     if request.method == 'PUT' or request.method == 'PATCH':
#         # save edits
#         mongo.db.threats.find_one_and_update({'_id': _id},
#                                              {'$set':
#                                                   {'type': _json["type"] if "type" in _json else "No type",
#                                                    'id': _json["type"] if "id" in _json else "No id",
#                                                    'created': _json[
#                                                        "created"] if "created" in _json else "No creation date",
#                                                    'modified': _json[
#                                                        "type"] if "modified" in _json else "No modifications",
#                                                    'object_marking_refs': _json[
#                                                        "object_marking_refs"] if "id" in _json else "No marking definitions",
#                                                    'name': _json["name"] if "name" in _json else "No name",
#                                                    'description': _json[
#                                                        "description"] if "description" in _json else "No description",
#                                                    'first_seen': _json[
#                                                        "first_seen"] if "first_seen" in _json else "No first seen date",
#                                                    'resource_level': _json[
#                                                        "resource_level"] if "resource_level" in _json else "No resource level",
#                                                    'primary_motivation': _json[
#                                                        "primary_motivation"] if "primary_motivation" in _json else "primary_motivation",
#                                                    'aliases': _json["aliases"] if "aliases" in _json else "aliases",
#                                                    'sophistication': _json[
#                                                        "sophistication"] if "sophistication" in _json else "sophistication",
#                                                    'pattern': _json["pattern"] if "pattern" in _json else "pattern",
#                                                    'roles': _json["roles"] if "roles" in _json else "roles",
#                                                    'labels': _json["labels"] if "labels" in _json else "labels",
#                                                    'external_references': _json[
#                                                        "external_references"] if "external_references" in _json else "external_references",
#                                                    'source_name': _json[
#                                                        "source_name"] if "source_name" in _json else "source_name",
#                                                    'url': _json["url"] if "url" in _json else "url",
#                                                    'external_id': _json[
#                                                        "external_id"] if "external_id" in _json else "external_id",
#                                                    'kill_chain_phases': _json[
#                                                        "kill_chain_phases"] if "kill_chain_phases" in _json else "kill_chain_phases",
#                                                    'kill_chain_name': _json[
#                                                        "kill_chain_name"] if "kill_chain_name" in _json else "kill_chain_name",
#                                                    'phase_name': _json[
#                                                        "phase_name"] if "phase_name" in _json else "phase_name",
#                                                    'relationship_type': _json[
#                                                        "relationship_type"] if "relationship_type" in _json else "relationship_type"},
#
#                                               })
#         resp = jsonify('STIX Document updated successfully!')
#         resp.status_code = 200
#         return resp
#     else:
#         # debugstr = 'method is ' + request.method + ' id is of type' + type(_id) + ' id is ' + _json['id']
#         debugstr = "something else"
#         message = {
#             'status': 404,
#             'message': debugstr,
#         }
#         resp = jsonify(message)
#         resp.status_code = 404
#         return resp
#

# @app.route('/demo_api/delete/<id>', methods=['DELETE'])
# def delete_documents(id):
#     mongo.db.threats.delete_one({'_id': ObjectId(id)})
#     # mongo.db.collection_name.delete_one({'_id': ObjectId(id)})
#     resp = jsonify('STIX Document deleted successfully!')
#     resp.status_code = 200
#     return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run('0.0.0.0', 5000, debug=True)
