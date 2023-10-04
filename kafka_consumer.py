from kafka_client import KafkaClient
from config import KAFKA_TOPIC
import json

kc = KafkaClient()


def process_message(message):
    key = message.key()
    d = json.loads(message.value())
    print(f'Received message with key: {key} and value: {d}')

    # download the photo
    # https://www.pinecone.io/learn/clip-image-search/#Implementation-of-CLIP-With-Python
    # create embedding of the photo along with text (use description)
    # send the embedding to pinecone along with metadata such as description and exif


def main():
    kc.consume(topic=KAFKA_TOPIC, process_message_callback=process_message)


if __name__ == "__main__":
    main()
