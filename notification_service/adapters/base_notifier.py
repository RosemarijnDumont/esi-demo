from abc import ABC, abstractmethod

class BaseNotifier(ABC):
    @abstractmethod
    def send(self, recipient: str, subject: str, message: str) -> bool:
        """
        Abstract method to send a notification.

        Args:
            recipient (str): The recipient of the notification (e.g., email address, phone number).
            subject (str): The subject of the notification.
            message (str): The content of the notification.

        Returns:
            bool: True if the notification was sent successfully, False otherwise.
        """
        pass