import json

from bson import json_util

from config import MONGO_DB_CONNECTION_STRING
from mongo_client import MongoClient
from kafka_client import KafkaClient, KafkaMessage


def main():
    mc = MongoClient(connection_string=MONGO_DB_CONNECTION_STRING)
    mc.connect()
    kc = KafkaClient()
    for document in mc.capture_changes():
        document_id = document["id"]
        encoded_value = json.dumps(document, default=json_util.default).encode('utf-8')
        kc.produce(KafkaMessage(key=document_id, value=encoded_value))
        print(f"Successfully sent document {document_id} to kafka topic")


if __name__ == "__main__":
    main()
