import logging
from notification_service.adapters.base_notifier import BaseNotifier
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotifier(BaseNotifier):
    def __init__(self, smtp_server: str = 'smtp.example.com', smtp_port: int = 587, sender_email: str = 'no-reply@example.com', sender_password: str = None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password # In production, use environment variables or a secure secret manager
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def send(self, recipient: str, subject: str, message: str) -> bool:
        log_prefix = f"Email notification to {recipient} for '{subject}' (via {self.smtp_server}:{self.smtp_port}): "
        logging.info(f"{log_prefix}Attempting to send.")
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls() # Secure the connection
                if self.sender_password:
                    server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            logging.info(f"{log_prefix}Successfully sent.")
            return True
        except Exception as e:
            logging.error(f"{log_prefix}Failed to send: {e}")
            return False
