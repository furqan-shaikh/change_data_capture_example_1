from dataclasses import dataclass
from typing import Any
import socket
from confluent_kafka import Producer, KafkaError, KafkaException, Consumer
from config import KAFKA_SERVERS, KAFKA_KEY, KAFKA_SECRET, KAFKA_SECURITY_PROTOCOL, KAFKA_TOPIC, KAFKA_CONSUMER_GROUP_ID


@dataclass
class KafkaMessage:
    key: Any
    value: Any


MIN_COMMIT_COUNT = 5


@dataclass
class KafkaClient:
    is_running = True

    def get_config(self):
        return {
            'bootstrap.servers': KAFKA_SERVERS,
            'security.protocol': KAFKA_SECURITY_PROTOCOL,
            'sasl.mechanism': 'PLAIN',
            'sasl.username': KAFKA_KEY,
            'sasl.password': KAFKA_SECRET,
            'client.id': socket.gethostname()
        }

    def produce(self, message: KafkaMessage):
        producer = Producer(self.get_config())
        producer.produce(KAFKA_TOPIC, key=message.key, value=message.value)
        producer.flush()

    def get_consumer(self):
        consumer_config = self.get_config()
        consumer_config['group.id'] = KAFKA_CONSUMER_GROUP_ID
        consumer = Consumer(consumer_config)
        return consumer

    def subscribe(self, topic):
        self.get_consumer().subscribe([topic])

    def consume(self, topic, process_message_callback):
        consumer = self.get_consumer()
        try:
            # 1. Subscribe to topic
            consumer.subscribe([topic])
            # 2. Start the consumer loop
            while self.is_running:
                # 3. Poll for new message
                message = consumer.poll(timeout=1.0)
                # 3.1 If no new message, continue
                if message is None:
                    print('No new message found. Continue to poll...')
                    continue
                # 3.2 If error, raise the exception
                if message.error():
                    if message.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        print('%% %s [%d] reached end at offset %d\n' %
                              (message.topic(), message.partition(), message.offset()))
                    elif message.error():
                        raise KafkaException(message.error())
                # 3.3 Process the message
                else:
                    print('New message found.')
                    process_message_callback(message)
                    # 4. Commit the offset. Ideally , commit should not be done on each message, but on a message batch
                    consumer.commit(asynchronous=False)
        finally:
            consumer.close()

    def stop_consuming(self):
        self.is_running = False
