import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def retry_notification_delivery(func, retries=5, initial_delay=1, backoff_factor=2):
    """
    Implements a retry mechanism with exponential backoff for notification delivery functions.

    Args:
        func (callable): The function to be retried (e.g., sending an email or in-app notification).
        retries (int): Maximum number of retries.
        initial_delay (int): Initial delay in seconds before the first retry.
        backoff_factor (int): Factor by which the delay increases after each failed attempt.

    Returns:
        Any: The result of the function if successful.

    Raises:
        Exception: If the function fails after all retries.
    """
    delay = initial_delay
    for i in range(retries):
        try:
            logging.info(f"Attempt {i+1}/{retries} to deliver notification.")
            return func()
        except Exception as e:
            logging.warning(f"Notification delivery failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= backoff_factor
    raise Exception(f"Notification delivery failed after {retries} attempts.")

# Example usage (for demonstration purposes)
# def send_email_notification(recipient, subject, body):
#     # Simulate email sending (can fail)
#     import random
#     if random.random() < 0.7:  # 70% chance of failure
#         raise ConnectionError("SMTP connection failed")
#     print(f"Email sent to {recipient}: {subject}")
#     return True

# def send_in_app_notification(user_id, message):
#     # Simulate in-app notification sending
#     import random
#     if random.random() < 0.6:  # 60% chance of failure
#         raise ValueError("In-app notification service unreachable")
#     print(f"In-app notification sent to user {user_id}: {message}")
#     return True

# if __name__ == "__main__":
#     print("\n--- Testing Email Notification Retry ---")
#     try:
#         # Using a lambda to pass arguments to the function being retried
#         result = retry_notification_delivery(lambda: send_email_notification("test@example.com", "Test Email", "Hello!"))
#         print(f"Email delivery successful: {result}")
#     except Exception as e:
#         print(f"Email delivery ultimately failed: {e}")

#     print("\n--- Testing In-App Notification Retry ---")
#     try:
#         result = retry_notification_delivery(lambda: send_in_app_notification("user123", "Your order has shipped!"))
#         print(f"In-app delivery successful: {result}")
#     except Exception as e:
#         print(f"In-app delivery ultimately failed: {e}")
