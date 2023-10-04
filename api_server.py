
from fastapi import FastAPI
from models import Photo, PhotoJSONEncoder
from config import MONGO_DB_CONNECTION_STRING
from mongo_client import MongoClient
import json


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/photos")
async def upload_photo(photo: Photo):
    photo_document = photo.to_dict()
    mc = MongoClient(connection_string=MONGO_DB_CONNECTION_STRING)
    mc.connect()
    mc.insert_to_photos_collection(documents=[photo_document])
    # kc = KafkaClient()
    # encoded_value = json.dumps(photo, default=json_util.default).encode('utf-8')
    # kc.produce(KafkaMessage(key=f"key-{photo.id}", value=encoded_value))
    # print('Sent to Kafka topic')
    return photo
