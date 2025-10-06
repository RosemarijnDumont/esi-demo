import smtplib
from email.mime.text import MIMEText
import os

def send_alert_email(subject, message, recipients):
    """Sends an alert email to a list of recipients."""
    sender_email = os.getenv("ALERT_SENDER_EMAIL")
    sender_password = os.getenv("ALERT_SENDER_PASSWORD") # Use App Password for Gmail, etc.
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    if not all([sender_email, sender_password, smtp_server]):
        print("Warning: Email alert configuration missing. Cannot send alert email.")
        return False

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls() # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, msg.as_string())
        print(f"[ALERT] Email alert '{subject}' sent successfully to {recipients}")
        return True
    except Exception as e:
        print(f"[ALERT_ERROR] Failed to send email alert: {e}")
        return False

def trigger_email_delivery_alert(customer_email, incident_details):
    """Triggers an alert for email delivery failures."""
    alert_recipients = os.getenv("ALERT_EMAIL_RECIPIENTS", "admin@example.com").split(',')
    subject = f"[ALERT] Email Delivery Failure to {customer_email}"
    message = f"Failed to deliver automated email to {customer_email}. Details: {incident_details}"
    send_alert_email(subject, message, alert_recipients)

def trigger_system_health_alert(service_name, status_info):
    """Triggers an alert for system health issues."""
    alert_recipients = os.getenv("ALERT_EMAIL_RECIPIENTS", "admin@example.com").split(',')
    subject = f"[ALERT] System Health Issue: {service_name} is Down"
    message = f"The service {service_name} is reporting an unhealthy status. Details: {status_info}"
    send_alert_email(subject, message, alert_recipients)

# Example usage:
# if __name__ == "__main__":
#     os.environ["ALERT_SENDER_EMAIL"] = "your_email@gmail.com"
#     os.environ["ALERT_SENDER_PASSWORD"] = "your_app_password"
#     os.environ["ALERT_EMAIL_RECIPIENTS"] = "devops@example.com,support@example.com"
#     trigger_email_delivery_alert("bademail@example.com", "Recipient inbox full.")
#     trigger_system_health_alert("CRM Service", "API not responding")
