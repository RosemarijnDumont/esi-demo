import time
import logging
import threading
from collections import deque

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NotificationService:
    def __init__(self, retry_limit=3, retry_delay=5):
        self.notification_queue = deque()
        self.retry_limit = retry_limit
        self.retry_delay = retry_delay
        self.processing_thread = threading.Thread(target=self._process_notifications, daemon=True)
        self._running = True
        self.processing_thread.start()
        logging.info("NotificationService initialized with retry_limit=%d and retry_delay=%d seconds.", retry_limit, retry_delay)

    def _send_notification_to_third_party(self, notification):
        """Simulates sending a notification to a third-party service.
        This method should be replaced with actual API calls to third-party services.
        """
        notification_id = notification['id']
        notification_type = notification['type']
        recipient = notification['recipient']
        content = notification['content']
        attempts = notification.get('attempts', 0)

        logging.info("Attempt %d: Sending %s notification (ID: %s) to %s - Content: %s",
                     attempts + 1, notification_type, notification_id, recipient, content)
        try:
            # Simulate network delay and potential failures
            if attempts == 0 and notification_id % 7 == 0:  # Simulate initial failure for some notifications
                raise ConnectionError("Simulated network hiccup")
            if attempts == 1 and notification_id % 13 == 0: # Simulate second failure
                raise TimeoutError("Simulated service timeout")
            
            time.sleep(1) # Simulate API call duration
            if notification_id % 5 == 0 and attempts < 2: # Simulate occasional success after retries
                logging.warning("Simulated partial success for notification ID %s. May require further checks.", notification_id)
                return False, "Simulated partial success"

            logging.info("Successfully sent %s notification (ID: %s) to %s.", notification_type, notification_id, recipient)
            return True, "Success"
        except (ConnectionError, TimeoutError, RuntimeError) as e:
            logging.warning("Failed to send %s notification (ID: %s) to %s: %s",
                            notification_type, notification_id, recipient, e)
            return False, str(e)

    def add_notification(self, notification_data):
        """Adds a new notification to the queue.
        Notification data should include 'id', 'type', 'recipient', 'content'.
        """
        if 'id' not in notification_data:
            notification_data['id'] = hash(frozenset(notification_data.items())) # Simple ID generation
        notification_data['attempts'] = 0
        notification_data['last_attempt_time'] = None
        self.notification_queue.append(notification_data)
        logging.info("Notification (ID: %s, Type: %s) added to queue.", notification_data['id'], notification_data['type'])

    def _process_notifications(self):
        """Worker thread method to process notifications from the queue.
        Implements retry mechanism.
        ""
        while self._running:
            if self.notification_queue:
                notification = self.notification_queue.popleft()
                notification_id = notification['id']
                notification_type = notification['type']
                recipient = notification['recipient']
                attempts = notification['attempts']

                logging.debug("Processing notification (ID: %s, Attempts: %d).", notification_id, attempts)

                success, message = self._send_notification_to_third_party(notification)

                if success:
                    logging.info("Notification (ID: %s, Type: %s) successfully delivered to %s after %d attempts.",
                                 notification_id, notification_type, recipient, attempts + 1)
                else:
                    if attempts < self.retry_limit:
                        notification['attempts'] += 1
                        notification['last_attempt_time'] = time.time()
                        self.notification_queue.append(notification) # Re-add to queue for retry
                        logging.warning("Notification (ID: %s, Type: %s) failed, retrying in %d seconds (Attempt %d/%d). Reason: %s",
                                        notification_id, notification_type, self.retry_delay, attempts + 1, self.retry_limit, message)
                        time.sleep(self.retry_delay) # Delay before next retry attempt for this notification
                    else:
                        logging.error("Notification (ID: %s, Type: %s) failed to deliver to %s after %d attempts. Giving up. Last reason: %s",
                                      notification_id, notification_type, recipient, attempts + 1, message)
            else:
                time.sleep(1) # Wait if queue is empty

    def stop(self):
        """Stops the notification processing thread.
        """
        logging.info("Stopping NotificationService...")
        self._running = False
        self.processing_thread.join()
        logging.info("NotificationService stopped.")

# Example Usage (for demonstration and testing)
if __name__ == "__main__":
    notification_service = NotificationService()

    # Simulate adding various notifications
    notification_service.add_notification({'type': 'email', 'recipient': 'user1@example.com', 'content': 'Welcome to our service!'})
    notification_service.add_notification({'type': 'in-app', 'recipient': 'user_id_2', 'content': 'Your report is ready.'})
    notification_service.add_notification({'type': 'sms', 'recipient': '+1234567890', 'content': 'Your order has shipped.'})
    notification_service.add_notification({'id': 7, 'type': 'email', 'recipient': 'user7@example.com', 'content': 'Critical alert: System maintenance.'}) # Will fail initially
    notification_service.add_notification({'id': 13, 'type': 'in-app', 'recipient': 'user_id_13', 'content': 'New feature available!'}) # Will fail twice
    notification_service.add_notification({'id': 5, 'type': 'email', 'recipient': 'user5@example.com', 'content': 'Special offer for you!'}) # Will show partial success
    notification_service.add_notification({'type': 'email', 'recipient': 'user8@example.com', 'content': 'Reminder: Your trial ends soon.'})


    # Let the service run for a while
    try:
        while True:
            time.sleep(5) # Keep the main thread alive
            if not notification_service.notification_queue:
                logging.info("Notification queue is empty. No more notifications to process.")
                # For demonstration, stop if queue is empty. In a real app, it would run indefinitely.
                # notification_service.stop()
                # break
    except KeyboardInterrupt:
        logging.info("Ctrl+C detected. Shutting down notification service.")
    finally:
        notification_service.stop()
