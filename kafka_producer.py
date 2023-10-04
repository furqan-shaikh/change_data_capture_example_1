from kafka_client import KafkaClient, KafkaMessage
import time
import json
from bson import json_util


def main():
    kc = KafkaClient()
    for i in range(1, 10):
        value = {
            "photo_id": str(i),
            "photo_url": f"https://unsplash.com/fushaikh/personal/{i}.jpg"
        }
        encoded_value = json.dumps(value, default=json_util.default).encode('utf-8')
        kc.produce(KafkaMessage(key=f"key-{i}", value=encoded_value))
        time.sleep(5)

if __name__ == "__main__":
    main()