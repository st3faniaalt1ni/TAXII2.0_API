# Taxii_api


We use medallion which is a prototype TAXII server implementation. As medallion is a prototype TAXII server implementation, the schema design for a Mongo DB is relatively straightforward. Its main purpose is for use in testing scenarios of STIX 2.0.It has been developed in conjunction with cti-taxii-client but should be compatible with any TAXII client which makes HTTP requests as defined in TAXII 2.0 specification.

# Installation Instructions and Usage


~~~
git clone https://github.com/st3faniaalt1ni/STIX2ToNeo4jDocManager.git
~~~

First, install the project dependencies:
~~~
pip install -r requirements.txt
~~~



# MongoDB configuration:

A mongodb running instance is required. 

Ensure that mongo is running a *replica set*. To initiate a replica set start mongo with:
~~~	 	 	 	
mongod  --port 27018 --replSet myDevReplSet
~~~
Then open mongo shell on port 27018 and run:
~~~
rs.initiate()
~~~

# For Neo4j docker Image:

Make sure that you have Docker and Docker-Compose installed.
Then run with sudo privileges:

~~~
docker run --name <container_name> -p7474:7474 -p7687:7687 -d -v /path/to/host/selected/directory/data:/data -v /path/to/host/selected/directory/logs:/logs -v /path/to/host/selected/directory/import:/var/lib/neo4j/import -v /path/to/host/selected/directory j/plugins:/plugins --env NEO4J_AUTH=<neo4j_instance_username>/< neo4j_instance_password> neo4j:latest
~~~


# For Neo4j-Doc-Manager:

You must have Python installed. Python 3 is recommended.
~~~
sudo apt install python3-pip
~~~

Then, install neo4j_doc_manager with pip3:
~~~
pip3 install neo4j-doc-manager
~~~
(You might need sudo privileges).


 Set  **NEO4J_AUTH** environment variable, containing  user and password. Username and password must be the same as the environment variables of neo4j container as they have been initiated on previous step.
~~~
export NEO4J_AUTH=<neo4j_instance_username>/< neo4j_instance_password>

~~~

Start the mongo-connector service with the following command:
~~~
mongo-connector -m localhost:27018 -t http://localhost:7474/db/data -d neo4j_doc_manager
~~~
**-m** provides Mongo endpoint
**-t** provides Neo4j endpoint. Be sure to specify the protocol (http).
**-d** specifies Neo4j Doc Manager.



# Data synchronization

With the REST API and the “neo4j_doc_manager” service running, Stix 2.0 JSON-based documents inserted into MongoDB will be converted into a graph structure and immediately inserted into Neo4j as well. Neo4j Doc Manager will turn keys into graph nodes. Nested values on each key will become properties.


# TAXII Server 
https://github.com/oasis-open/cti-taxii-server

# TAXII_api
We initialise  TAXII_ api and make an authorized user


# Visualisation (Optional):

Postman can be used for HTTP requests  and Mongo Compass for TAXII collections in MongoDB 
