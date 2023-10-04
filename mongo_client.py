from dataclasses import dataclass
import pymongo
from typing import Any
import urllib.parse
from config import MONGO_DB_USERNAME, MONGO_DB_PASSWORD, MONGO_DB_NAME, MONGO_DB_PHOTO_COLLECTION


@dataclass
class MongoClient:
    connection_string: str
    client: Any = None

    def __post_init__(self):
        username = urllib.parse.quote_plus(MONGO_DB_USERNAME)
        password = urllib.parse.quote_plus(MONGO_DB_PASSWORD)
        self.connection_string = self.connection_string.replace('<u>:<p>', f'{username}:{password}')
        print(self.connection_string)

    def connect(self):
        try:
            self.client = pymongo.MongoClient(self.connection_string)
            print('Successfully connected to mongo server: ', self.client)
        except pymongo.errors.ConfigurationError as e:
            print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
            raise Exception(str(e))

    def insert_to_photos_collection(self, documents):
        db = self.client[MONGO_DB_NAME]
        photos_collection = db[MONGO_DB_PHOTO_COLLECTION]
        try:
            result = photos_collection.insert_many(documents)
            print('Added document to collection: ', result)
        except pymongo.errors.OperationFailure as e:
            print(
                "An authentication error was received. Are you sure your database user is authorized to perform write operations?")
            raise Exception(str(e))
        except Exception as e:
            raise e

    def capture_changes(self):
        db = self.client[MONGO_DB_NAME]
        photos_collection = db[MONGO_DB_PHOTO_COLLECTION]
        change_stream = photos_collection.watch()
        for change in change_stream:
            if change['operationType'] == 'insert':
                document = change['fullDocument']
                yield document

