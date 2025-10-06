import logging
from notification_service.retry_mechanism import retry_notification_delivery
from notification_service.health_checks import NotificationHealthChecker
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Placeholder for actual third-party service integrations ---
class EmailService:
    def send_email(self, recipient, subject, body):
        logging.info(f"Attempting to send email to {recipient} with subject '{subject}'...")
        # Simulate success/failure for demonstration
        import random
        if random.random() < 0.2:  # 20% failure rate
            raise ConnectionError("Failed to connect to email sending service")
        logging.info(f"Successfully sent email to {recipient}.")
        return {"status": "sent", "service_id": "email-svc-123"}

class SMSService:
    def send_sms(self, phone_number, message):
        logging.info(f"Attempting to send SMS to {phone_number}...")
        # Simulate success/failure for demonstration
        import random
        if random.random() < 0.1:  # 10% failure rate
            raise TimeoutError("SMS gateway timed out")
        logging.info(f"Successfully sent SMS to {phone_number}.")
        return {"status": "sent", "service_id": "sms-svc-456"}

class InAppNotificationService:
    def send_in_app_notification(self, user_id, message, notification_type="info"):
        logging.info(f"Attempting to send in-app notification to user {user_id} ({notification_type})...")
        # Simulate success/failure for demonstration
        import random
        if random.random() < 0.05:  # 5% failure rate
            raise ValueError("In-app notification system error")
        logging.info(f"Successfully sent in-app notification to user {user_id}.")
        return {"status": "sent", "notification_id": "inapp-notif-789"}


class NotificationManager:
    """
    Manages the generation, sending, retry, and monitoring of all notification types.
    """
    def __init__(self):
        self.email_service = EmailService()
        self.sms_service = SMSService()
        self.in_app_service = InAppNotificationService()

        self.notification_queues = ["email-queue-critical", "email-queue-marketing", "inapp-queue-priority", "inapp-queue-general"]
        self.notification_workers = ["email-worker-1", "email-worker-2", "inapp-worker-1", "inapp-worker-2"]
        self.health_checker = NotificationHealthChecker(self.notification_queues, self.notification_workers)

    def _audit_and_check_third_party_integrations(self):
        """
        Audits notification generation/sending pipelines and checks third-party integrations.
        In a real system, this would involve querying logs, metrics, or vendor APIs.
        For this implementation, it will just log a status.
        """
        logging.info("--- Auditing Notification Pipelines and Third-Party Integrations ---")
        # Placeholder for actual audit and integration status checks.
        # E.g., check email service API rate limits, SMS delivery reports, etc.
        email_integration_healthy = True # Assume healthy for now
        sms_integration_healthy = True   # Assume healthy for now
        inapp_integration_healthy = True # Assume healthy for now

        if not email_integration_healthy:
            logging.error("Email service integration is experiencing issues (e.g., high error rates, delivery delays).")
        if not sms_integration_healthy:
            logging.error("SMS service integration is experiencing issues.")
        if not inapp_integration_healthy:
            logging.error("In-app notification service integration is experiencing issues.")

        logging.info("Notification pipeline audit completed. See above for any warnings/errors.")

    def send_notification(self, notification_type, **kwargs):
        """
        Sends a notification of a given type, utilizing retry mechanisms.

        Args:
            notification_type (str): Type of notification ('email', 'sms', 'in-app').
            **kwargs: Arguments specific to the notification type.

        Returns:
            dict: The result of the notification sending attempt.
        """
        logging.info(f"Attempting to send {notification_type} notification...")
        try:
            if notification_type == "email":
                recipient = kwargs.get("recipient")
                subject = kwargs.get("subject")
                body = kwargs.get("body")
                if not all([recipient, subject, body]):
                    raise ValueError("Missing required fields for email notification.")
                result = retry_notification_delivery(lambda: self.email_service.send_email(recipient, subject, body))
            elif notification_type == "sms":
                phone_number = kwargs.get("phone_number")
                message = kwargs.get("message")
                if not all([phone_number, message]):
                    raise ValueError("Missing required fields for SMS notification.")
                result = retry_notification_delivery(lambda: self.sms_service.send_sms(phone_number, message))
            elif notification_type == "in-app":
                user_id = kwargs.get("user_id")
                message = kwargs.get("message")
                notification_display_type = kwargs.get("notification_display_type", "info") # default to info
                if not all([user_id, message]):
                    raise ValueError("Missing required fields for in-app notification.")
                result = retry_notification_delivery(lambda: self.in_app_service.send_in_app_notification(user_id, message, notification_display_type))
            else:
                raise ValueError(f"Unknown notification type: {notification_type}")

            logging.info(f"Successfully processed {notification_type} notification: {result}")
            return result
        except Exception as e:
            logging.error(f"Failed to send {notification_type} notification after multiple retries: {e}")
            return {"status": "failed", "error": str(e)}

    def run_daily_checks_and_audits(self):
        """
        Runs a comprehensive set of daily checks including health checks and audits.
        This method should be called periodically by a scheduler.
        """
        logging.info("\n--- Running DAILY Notification Service Checks and Audits ---")
        self._audit_and_check_third_party_integrations()
        self.health_checker.run_all_health_checks()
        logging.info("--- Daily Notification Service Checks and Audits Completed ---")


# --- End-to-End Testing (for demonstration) ---
def run_end_to_end_tests(manager):
    logging.info("\n=== Running End-to-End Notification Tests ===")

    print("\n--- Test Case 1: Successful Email Notification ---")
    email_result = manager.send_notification(
        "email",
        recipient="user@example.com",
        subject="Welcome to Our Service!",
        body="Thank you for registering."
    )
    print(f"Test Case 1 Result: {email_result}\n")

    print("\n--- Test Case 2: Failed Email Notification (simulated multiple retries) ---")
    # Temporarily increase failure rate for this test
    original_email_fail_rate = manager.email_service.send_email # Store original
    def always_fail(*args, **kwargs):
        raise ConnectionRefusedError("Simulated persistent email failure")
    manager.email_service.send_email = always_fail
    email_fail_result = manager.send_notification(
        "email",
        recipient="fail@example.com",
        subject="Critical Alert",
        body="System experiencing high load."
    )
    manager.email_service.send_email = original_email_fail_rate # Restore original
    print(f"Test Case 2 Result: {email_fail_result}\n")

    print("\n--- Test Case 3: Successful In-App Notification ---")
    in_app_result = manager.send_notification(
        "in-app",
        user_id="user123",
        message="Your dashboard has been updated.",
        notification_display_type="update"
    )
    print(f"Test Case 3 Result: {in_app_result}\n")

    print("\n--- Test Case 4: SMS Notification with retry ---")
    sms_result = manager.send_notification(
        "sms",
        phone_number="+15551234567",
        message="Your verification code is 12345."
    )
    print(f"Test Case 4 Result: {sms_result}\n")

    print("\n=== End-to-End Notification Tests Completed ===")


if __name__ == "__main__":
    notification_manager = NotificationManager()

    # Run daily checks and audits
    notification_manager.run_daily_checks_and_audits()

    # Run end-to-end tests for various user actions
    run_end_to_end_tests(notification_manager)

    # Simulate a user action triggering notifications
    print("\n--- Simulating User Action: New User Registration ---")
    # In a real application, this would be called by the user service or an event listener.
    user_email = "newuser@example.com"
    user_id = "user_new_456"

    # Send welcome email (async in a real system)
    notification_manager.send_notification(
        "email",
        recipient=user_email,
        subject="Welcome Aboard!",
        body="We are thrilled to have you join our community."
    )

    # Send in-app notification
    notification_manager.send_notification(
        "in-app",
        user_id=user_id,
        message="Welcome! Explore your new dashboard.",
        notification_display_type="welcome"
    )

    print("\n--- Simulating User Action: Password Reset ---")
    reset_email = "testuser@example.com"
    reset_user_id = "user_test_123"
    reset_phone = "+15559876543"

    notification_manager.send_notification(
        "email",
        recipient=reset_email,
        subject="Password Reset Request",
        body="You requested a password reset. Follow this link..."
    )
    notification_manager.send_notification(
        "sms",
        phone_number=reset_phone,
        message="Your password reset code is 67890."
    )
    notification_manager.send_notification(
        "in-app",
        user_id=reset_user_id,
        message="A password reset email has been sent to your registered email address."
    )

    # Run checks again after some operations
    print("\n--- Running post-action checks ---")
    notification_manager.run_daily_checks_and_audits()

