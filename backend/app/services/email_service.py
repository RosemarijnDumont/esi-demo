import os
import jinja2
from typing import Dict, Any, Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from backend.app.crud import email_automation as crud
from backend.app.db.session import SessionLocal
from backend.app.schemas.email_automation import EmailLogCreate

class EmailService:
    def __init__(self):
        self.sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        self.sender_email = os.getenv("SENDER_EMAIL", "noreply@example.com")

    def _render_template(self, template_content: str, context: Dict[str, Any]) -> str:
        env = jinja2.Environment(loader=jinja2.BaseLoader())
        template = env.from_string(template_content)
        return template.render(context)

    def send_email(
        self, 
        recipient_email: str, 
        subject: str, 
        body: str, 
        template_id: Optional[int] = None,
        automation_rule_id: Optional[int] = None
    ) -> Dict[str, Any]:
        if not self.sendgrid_api_key:
            # Log and simulate email sending in development without SendGrid key
            print(f"Warning: SENDGRID_API_KEY not set. Simulating email to {recipient_email}")
            print(f"Subject: {subject}")
            print(f"Body: {body}")
            status = "SIMULATED"
            error_message = "SENDGRID_API_KEY not set"
        else:
            message = Mail(
                from_email=self.sender_email,
                to_emails=recipient_email,
                subject=subject,
                html_content=body
            )
            try:
                sendgrid_client = SendGridAPIClient(self.sendgrid_api_key)
                response = sendgrid_client.send(message)
                status = "SENT" if response.status_code == 202 else "FAILED"
                error_message = None if response.status_code == 202 else response.body.decode()
                print(f"Email sent via SendGrid. Status Code: {response.status_code}")
            except Exception as e:
                status = "FAILED"
                error_message = str(e)
                print(f"Error sending email via SendGrid: {e}")

        # Log the email attempt
        with SessionLocal() as db:
            email_log_create = EmailLogCreate(
                recipient_email=recipient_email,
                subject=subject,
                body_sent=body,
                template_id=template_id,
                automation_rule_id=automation_rule_id,
                status=status,
                error_message=error_message
            )
            crud.create_email_log(db=db, email_log=email_log_create)

        return {"status": status, "error_message": error_message}

    def send_templated_email(
        self, 
        template_id: int, 
        recipient_email: str, 
        context: Dict[str, Any],
        automation_rule_id: Optional[int] = None
    ) -> Dict[str, Any]:
        with SessionLocal() as db:
            template = crud.get_email_template(db, template_id)
            if not template:
                raise ValueError(f"Email template with ID {template_id} not found.")

            subject = self._render_template(template.subject, context)
            body = self._render_template(template.body, context)

            return self.send_email(
                recipient_email=recipient_email,
                subject=subject,
                body=body,
                template_id=template_id,
                automation_rule_id=automation_rule_id
            )

email_service = EmailService()
