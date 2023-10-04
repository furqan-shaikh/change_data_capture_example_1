This is a sample application to implement Change Data Capture pattern using MongoDb and Kafka.

# High Level Architecture
![hla.png](docs%2Fhla.png)

# Flow
1. User posts a new document by invoking the POST method on a FastAPI-based REST API Server
2. Store the document in a Mongodb collection
    2.a This new document needs to be made available in a downstream system using Change Data Capture pattern
    2.b This allows us to now explicitly call a downstream system(s)
3. Change Stream Listener listens to any `insert` operations in a MongoDb collection using MongoDb Change Streams API
4. Change Stream Listener on receiving a new document notification, pushes the document to a Kafka Topic
5. Kafka Consumers (part of a Kafka Consumer Group) poll for new messages from the topic
6. On receiving a new message, send the document to the downstream system
    6.a Using Kafka Consumer Group, we can spin up multiple Consumer Groups per downstream system

# Running the application
1. Add required values in `config.py`
2. Make sure to have a running MongoDb and Kafka clusters.
   - 2.a For this application, I am using MongoDb Atlas and Confluent Kafka hosted offerings
3. Run: `bash start.sh`

# References
- https://www.mongodb.com/developer/languages/python/python-change-streams/ - MongoDB Change Streams with Python
- https://pymongo.readthedocs.io/en/stable/examples/authentication.html - Pymongo Authentication Examples
- https://docs.confluent.io/kafka-clients/python/current/overview.html - Kafka Python client