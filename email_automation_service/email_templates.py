
class EmailTemplates:
    """
    Manages the email templates for various inquiry types.
    Templates are customizable and can be expanded as needed.
    """
    def __init__(self):
        self.templates = {
            "password_reset_confirmation": {
                "subject": "Your Password Reset Request - Action Required",
                "body": (
                    "Dear {customer_name},\n\n"
                    "We received a request to reset your password for your account associated with inquiry {inquiry_id}. "
                    "If you made this request, please follow the instructions sent to your registered email address.\n\n"
                    "If you did not request a password reset, please ignore this email or contact support immediately.\n\n"
                    "Thank you,\nYour Support Team"
                )
            },
            "billing_acknowledgement": {
                "subject": "Regarding Your Billing Inquiry - Inquiry #{inquiry_id}",
                "body": (
                    "Dear {customer_name},\n\n"
                    "Thank you for contacting us regarding your billing inquiry for inquiry #{inquiry_id} (Subject: '{inquiry_subject}'). "
                    "We have received your message and our billing department is currently reviewing it. "
                    "We aim to respond within 24-48 business hours.\n\n"
                    "In the meantime, you might find answers to common billing questions in our FAQ section: [Link to FAQ]\n\n"
                    "Sincerely,\nYour Support Team"
                )
            },
            "order_status_acknowledgement": {
                "subject": "Update on Your Order Status Inquiry - Inquiry #{inquiry_id}",
                "body": (
                    "Dear {customer_name},\n\n"
                    "Thank you for reaching out about your order status for inquiry #{inquiry_id} (Subject: '{inquiry_subject}'). "
                    "We are currently checking the details of your order and will provide an update shortly. "
                    "You can also track your order directly here: [Link to Order Tracking] with your order number.\n\n"
                    "We appreciate your patience.\n\n"
                    "Best regards,\nYour Support Team"
                )
            },
            "feature_request_acknowledgement": {
                "subject": "Your Feature Request Has Been Received - Inquiry #{inquiry_id}",
                "body": (
                    "Dear {customer_name},\n\n"
                    "Thank you for your valuable feedback and for submitting a feature request via inquiry #{inquiry_id} (Subject: '{inquiry_subject}'). "
                    "We are always looking for ways to improve our product, and your suggestions are important to us. "
                    "While we can't implement every request, your input helps us prioritize future developments.\n\n"
                    "We appreciate you helping us make our product better!\n\n"
                    "Sincerely,\nYour Product Team"
                )
            }
        }

    def get_template_subject(self, template_name: str) -> str | None:
        """
        Returns the subject line for a given template name.
        """
        return self.templates.get(template_name, {}).get("subject")

    def get_template_body(self, template_name: str) -> str | None:
        """
        Returns the body content for a given template name.
        """
        return self.templates.get(template_name, {}).get("body")
