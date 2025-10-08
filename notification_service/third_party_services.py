
import os
from typing import Dict, Any
import httpx

# --- Email Service Provider (e.g., SendGrid) ---
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_SENDER_EMAIL = os.getenv("SENDGRID_SENDER_EMAIL", "noreply@example.com")

async def send_email_with_provider(to_email: str, subject: str, html_content: str) -> Dict[str, Any]:
    if not SENDGRID_API_KEY:
        print("SENDGRID_API_KEY not set. Skipping actual email sending.")
        return {"status": "skipped", "message": "SENDGRID_API_KEY not configured"}

    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "personalizations": [
            {
                "to": [{"email": to_email}],
                "subject": subject,
            }
        ],
        "from": {"email": SENDGRID_SENDER_EMAIL},
        "content": [
            {
                "type": "text/html",
                "value": html_content,
            }
        ],
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            print(f"Email sent successfully to {to_email} via SendGrid")
            return {"status": "success", "response": response.json() if response.status_code != 204 else {}}
        except httpx.HTTPStatusError as e:
            print(f"Error sending email: {e.response.status_code} - {e.response.text}")
            raise Exception(f"SendGrid API error: {e.response.text}")
        except httpx.RequestError as e:
            print(f"Network error sending email: {e}")
            raise Exception(f"Network error: {e}")

# --- Other potential third-party integrations (e.g., Push notifications, SMS) can be added here ---
