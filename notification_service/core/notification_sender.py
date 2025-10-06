import logging
from notification_service.adapters.base_notifier import BaseNotifier
from notification_service.data.data_store import DataStore

class NotificationSender:
    def __init__(self, notifier: BaseNotifier, max_retries: int = 3, retry_delay: int = 60):
        self.notifier = notifier
        self.max_retries = max_retries
        self.retry_delay = retry_delay # seconds
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def send_notification(self, recipient: str, subject: str, message: str, task_id: str) -> bool:
        """
        Sends a notification and handles retries.
        Logs the delivery attempt and status.
        """
        for attempt in range(self.max_retries):
            logging.info("Attempt %d to send notification for task_id: %s to recipient: %s via %s", 
                         attempt + 1, task_id, recipient, self.notifier.__class__.__name__)
            try:
                success = self.notifier.send(recipient, subject, message)
                if success:
                    log_entry = {
                        "task_id": task_id,
                        "recipient": recipient,
                        "channel": self.notifier.__class__.__name__,
                        "subject": subject,
                        "status": "sent",
                        "attempt": attempt + 1
                    }
                    DataStore.log_hcat_delivery(log_entry)
                    logging.info("Notification successfully sent for task_id: %s in %d attempts", task_id, attempt + 1)
                    return True
            except Exception as e:
                logging.error("Error sending notification for task_id: %s (Attempt %d): %s", task_id, attempt + 1, e)

            if attempt < self.max_retries - 1:
                logging.warning("Retrying notification for task_id: %s in %d seconds...", task_id, self.retry_delay)
                # In a real application, you'd want a non-blocking delay or use something like Celery for retries
                # For this synchronous example, we'll just log the intent to retry.
                # time.sleep(self.retry_delay) # Not ideal for a web server, but demonstrates the concept.

        log_entry = {
            "task_id": task_id,
            "recipient": recipient,
            "channel": self.notifier.__class__.__name__,
            "subject": subject,
            "status": "failed",
            "attempts": self.max_retries
        }
        DataStore.log_hcat_delivery(log_entry)
        logging.error("Failed to send notification for task_id: %s after %d attempts", task_id, self.max_retries)
        return False