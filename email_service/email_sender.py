import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To
from jinja2 import Environment, FileSystemLoader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self, api_key, sender_email, template_dir="email_service/templates"):
        self.sg = SendGridAPIClient(api_key)
        self.sender = Email(sender_email)
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def send_email(self, recipient_email, subject, template_name, template_data):
        try:
            template = self.env.get_template(template_name)
            html_content = template.render(**template_data)

            message = Mail(
                from_email=self.sender,
                to_emails=To(recipient_email),
                subject=subject,
                html_content=html_content
            )

            response = self.sg.send(message)

            logger.info(f"Email sent to {recipient_email} with subject '{subject}'. Status Code: {response.status_code}")
            logger.debug(f"SendGrid Response Body: {response.body}")
            logger.debug(f"SendGrid Response Headers: {response.headers}")
            return response

        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {e}")
            return None

    def track_delivery(self, message_id):
        # In a real-world scenario, you'd integrate with SendGrid's Event Webhook
        # to get delivery, open, and click metrics asynchronously.
        # This method is a placeholder to demonstrate the concept.
        logger.info(f"Tracking delivery status for message_id: {message_id}. This would typically be handled via webhooks.")
        return {"status": "tracking_pending", "message_id": message_id}

if __name__ == '__main__':
    # Example Usage:
    # Set your SendGrid API Key as an environment variable
    # export SENDGRID_API_KEY='YOUR_SENDGRID_API_KEY'

    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
    if not sendgrid_api_key:
        logger.error("SENDGRID_API_KEY environment variable not set.")
        exit(1)

    email_sender = EmailSender(api_key=sendgrid_api_key, sender_email="no-reply@yourcompany.com")

    # Example 1: Send a support ticket acknowledgment
    email_sender.send_email(
        recipient_email="customer@example.com",
        subject="Your Support Ticket Has Been Received (Example)",
        template_name="example_template.html",
        template_data={
            "customer_name": "John Doe",
            "ticket_id": "ABC-123-XYZ"
        }
    )

    # Example 2: Send a password reset email
    email_sender.send_email(
        recipient_email="user@example.com",
        subject="Password Reset Request (Example)",
        template_name="forgot_password_template.html",
        template_data={
            "customer_name": "Jane Smith",
            "reset_link": "https://yourcompany.com/reset-password/token12345"
        }
    )

    # Example of tracking (conceptual)
    email_sender.track_delivery("some_message_id_from_sendgrid")
