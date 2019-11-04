# TAXII2.0_API


We use medallion which is a prototype TAXII server implementation.TAXII 2.0 Server implemented in Flask with MongoDB backend.Its main purpose is for use in testing scenarios of STIX 2.0.It has been developed in conjunction with cti-taxii-client but should be compatible with any TAXII client which makes HTTP requests as defined in TAXII 2.0 specification.

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




# TAXII Server 
 Follow the installation instructions for the Medallion TAXII Server Implementation
 https://github.com/oasis-open/cti-taxii-server.git

~~~ 
 [ ] Clone medallion
git clone https://github.com/oasis-open/cti-taxii-server.git

cd cti-taxii-server
pip3 install -r requirements

To run
python3 medallion/scripts/run --port <PORT TO RUN> --log-level <DEBUG> <configuration json file>
~~~ 
 
 
# TAXII Client
 Follow the installation instructions for the minimal client implementation for the TAXII 2.0 server
 https://github.com/oasis-open/cti-taxii-server.git
 
 ~~~
 pip3 install taxii2-client
 
 python3
 
 from taxii2client import Server
 server = Server('https://example.com/taxii/', user='user_id', password='user_password')
 ~~~
 
 


# TAXII_API
Initialise  TAXII_API 
~~~
python3 api_db_setup.py 
python3 main.py 
~~~

Create user and authentication credentials to access the server
~~~
python3 auth_db_utils.py --user
~~~

# Visualisation (Optional):
Postman can be used for HTTP requests  and Mongo Compass for TAXII collections in MongoDB 
