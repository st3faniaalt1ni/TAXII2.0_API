# TAXII2.0_API


We use medallion which is a prototype TAXII server implementation.TAXII 2.0 Server is implemented in Python with MongoDB backend and usage of Flask library.Its main purpose is for testing and demonstrating scenarios of STIX 2.0.It has been developed in conjunction with cti-taxii-client but should be compatible with any TAXII client which makes HTTP requests as defined in TAXII 2.0 specification.

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
export NEO4J_AUTH=<neo4j_instance_username>:< neo4j_instance_password>

~~~

Start the mongo-connector service with the following command:
~~~
mongo-connector -m localhost:27018 -t http://localhost:7474/db/data -d neo4j_doc_manager
~~~
**-m** provides Mongo endpoint
**-t** provides Neo4j endpoint. Be sure to specify the protocol (http).
**-d** specifies Neo4j Doc Manager.


# TAXII Server 

 Follow the installation instructions for the Medallion TAXII Server Implementation
 https://github.com/oasis-open/cti-taxii-server.git

Clone medallion and install required packages
~~~ 
git clone https://github.com/oasis-open/cti-taxii-server.git

cd cti-taxii-server
pip3 install -r requirements.txt
~~~
To run
~~~
python3 medallion/scripts/run --port <PORT TO RUN> --log-level <DEBUG> <configuration json file>
~~~ 
 

Create user and authentication credentials to have  permission to access the server. To create the user credentials use the script available at cti-taxii-server/medallion/scripts/auth_db_utils
~~~
python3 auth_db_utils.py --user
~~~

# TAXII_API
Initialize  TAXII_API mongodb backend with demo data
~~~
python3 api_db_setup_medallion.py 
~~~

# TAXII Client
 
 ~~~
 pip3 install taxii2-client
 ~~~
 




After having created the appropriate credentials you can get information about TAXII Server, available Api's  and TAXII Collections, import a new TAXII collection in your Api or/and import STIX stream data as bundles in a collection.
~~~
python3 api_client_info_demo.py
~~~
~~~
python3 api_db_new_collection.py 
~~~
~~~
python3 api_client_post_demo.py 
~~~

# Visualisation (Optional):
Postman can be used for visualisation of TAXII Endpoints  and MongoDB Compass  for TAXII collections in MongoDB. Further Neo4j frontend can be used for graph cypher queries.
