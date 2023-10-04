from config import MONGO_DB_CONNECTION_STRING
from mongo_client import MongoClient


def main():
    mc = MongoClient(connection_string=MONGO_DB_CONNECTION_STRING)
    mc.connect()
    # for i in range(1, 5):
    mc.insert_to_photos_collection(documents=[{"id": 1}])


if __name__ == "__main__":
    main()
