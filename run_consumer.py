
import asyncio
from notification_service.kafka_consumer_worker import consume_notifications

if __name__ == "__main__":
    print("Starting Notification Service Kafka Consumer...")
    asyncio.run(consume_notifications())
