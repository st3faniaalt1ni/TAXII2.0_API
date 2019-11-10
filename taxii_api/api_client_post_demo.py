from taxii2client import Server,Collection,ApiRoot, Status
import json
from datetime import datetime
import dateutil.parser


def manifest_find_object_by_id(manifest,id):
    for obj in manifest['objects']:
        if id in obj['id']:
            return obj
    return None

if __name__ == "__main__":
    server = Server('http://localhost:8090/taxii', user='it06156@uom.edu.gr', password='sa1234!@')

    print("Server title : %s"% server.title)
    collection = Collection('http://localhost:8090/demo_api/collections/f45753b6-d69c-48b3-97e1-20a8de4c178b', user='it06156@uom.edu.gr', password='sa1234!@')
    print('Description : %s'%collection.description)


    with open('apt1.json', encoding='utf-8') as json_file:
        stix_bundle = json.load(json_file)

    print('JSON file :')
    print('description : %s'%stix_bundle['type'])
    print('Objects included : %d'%len(stix_bundle['objects']))
    print('--------------------')
    print('Adding bundle to TAXII server..')
    request_status = collection.add_objects(stix_bundle)

    print('REQUEST STATUS')
    request_datetime = dateutil.parser.parse(request_status.request_timestamp)
    request_datetime_string = request_datetime.strftime('%Y-%m-%d %H:%M.%S')
    print('request received at %s'%request_datetime_string)
    print('request url : %s'%request_status.url)
    print('Total count of objects : %d'%request_status.total_count)
    print('Suceeded requests : %d'%request_status.success_count)
    print('Failed requests : %d'%request_status.failure_count)
    print('Request status: %s'%request_status.status)

    print('Info of each inserted object')

    manifest = collection.get_manifest()

    for id in request_status.successes:
        object = collection.get_object(id)
        try:
            name = object['objects'][0]['name']
        except KeyError:
            name = 'Field not specified'
        print('Name: %s'%name)
        try:
            type = object['objects'][0]['type']
        except KeyError:
            type = 'Field not specified'
        print('type: %s'%type)
        try:
            description = object['objects'][0]['description']
        except KeyError:
            description = 'Field not specified'
        print('description: %s'%description)

        print('ID : %s'%id)
        try:
            first_seen = object['objects'][0]['first_seen']
            first_seen_datetime = dateutil.parser.parse(first_seen)
            first_seen_string = first_seen_datetime.strftime('%Y-%m-%d @ %H:%M')
        except KeyError:
            first_seen_string = 'Field not specified'
        print('First seen: %s'%first_seen_string)
        try:
            created = object['objects'][0]['created']
            created_datetime = dateutil.parser.parse(created)
            created_string = created_datetime.strftime('%Y-%m-%d @ %H:%M')
        except KeyError:
            created_string = 'Field not specified'
        print('Created: %s'%created_string)
        # Retrieve object metadata from manifest
        manifest_object = manifest_find_object_by_id(manifest,id)
        if manifest_object is not None:
            date_added = dateutil.parser.parse(manifest_object['date_added'])
            date_added_string = date_added.strftime('%Y-%m-%d %H:%M.%S')
            print('Object added to the collection : %s'%date_added_string)
        print('---------------------------------------------------------------')
