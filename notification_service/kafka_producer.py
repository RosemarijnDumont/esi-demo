
from aiokafka import AIOKafkaProducer
import asyncio
import json
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "notifications")

kafka_producer = None

async def get_kafka_producer():
    global kafka_producer
    if kafka_producer is None:
        kafka_producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await kafka_producer.start()
    return kafka_producer

async def send_notification_to_kafka(notification_id: int, notification_type: str, recipient: str, template_name: str, template_data: dict, retries_attempted: int = 0):
    producer = await get_kafka_producer()
    message = {
        "notification_id": notification_id,
        "notification_type": notification_type,
        "recipient": recipient,
        "template_name": template_name,
        "template_data": template_data,
        "retries_attempted": retries_attempted
    }
    await producer.send_and_wait(KAFKA_TOPIC, json.dumps(message).encode('utf-8'))
    print(f"Sent notification {notification_id} to Kafka topic {KAFKA_TOPIC}")

async def close_kafka_producer():
    global kafka_producer
    if kafka_producer:
        await kafka_producer.stop()
        kafka_producer = None
