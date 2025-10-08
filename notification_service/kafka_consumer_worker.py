
from aiokafka import AIOKafkaConsumer
import asyncio
import json
import os
import httpx # For making HTTP requests to the FastAPI service

from jinja2 import Environment, FileSystemLoader

from .third_party_services import send_email_with_provider
from .template_manager import render_template

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "notifications")
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8000") # URL of your FastAPI service

async def consume_notifications():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="notification-service-group",
        auto_offset_reset="earliest"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Consumed message: topic={msg.topic}, partition={msg.partition}, offset={msg.offset}, value={msg.value.decode()}")
            notification_data = json.loads(msg.value.decode())
            await process_notification(notification_data)
    finally:
        await consumer.stop()

async def process_notification(notification_data: dict):
    notification_id = notification_data.get("notification_id")
    notification_type = notification_data.get("notification_type")
    recipient = notification_data.get("recipient")
    template_name = notification_data.get("template_name")
    template_data = notification_data.get("template_data", {})
    retries_attempted = notification_data.get("retries_attempted", 0)

    print(f"Processing notification {notification_id} for {recipient} (Type: {notification_type})")

    status = "sent"
    details = "Notification sent successfully"
    try:
        rendered_content = await render_template(template_name, template_data)

        # In a real application, you'd fetch user preferences here to decide if sending is allowed.
        # For this example, we'll proceed based on notification_type.
        
        if notification_type == "email":
            await send_email_with_provider(recipient, f"Subject: {template_name}", rendered_content)
        elif notification_type == "in-app":
            # For in-app, we would typically push to a websocket or another in-app delivery mechanism
            # For now, we'll just log it as 'sent'
            print(f"Simulating in-app notification for {recipient}: {rendered_content}")
        else:
            status = "failed"
            details = f"Unknown notification type: {notification_type}"
            print(details)

    except Exception as e:
        status = "failed"
        details = str(e)
        print(f"Error processing notification {notification_id}: {e}")

    # Hitting an internal endpoint to update the status and handle retries
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{NOTIFICATION_SERVICE_URL}/_internal/notifications/process",
                json={
                    "notification_id": notification_id,
                    "status": status,
                    "details": details,
                    "retries_attempted": retries_attempted
                }
            )
            response.raise_for_status()
            print(f"Updated notification {notification_id} status to {status}")
        except httpx.HTTPStatusError as e:
            print(f"Error updating notification status for {notification_id}: {e.response.text}")
        except httpx.RequestError as e:
            print(f"Network error updating notification status for {notification_id}: {e}")

if __name__ == "__main__":
    # This block is for running the consumer directly for testing/development
    # In production, this would likely be run as a separate process or container
    print(f"Starting Kafka consumer for topic: {KAFKA_TOPIC} on {KAFKA_BOOTSTRAP_SERVERS}")
    asyncio.run(consume_notifications())
