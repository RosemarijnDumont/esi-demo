
import os
import json
import logging
from flask import Flask, request, jsonify
from support_platform_api import SupportPlatformAPI  # Assuming this exists based on step 1
from email_service_provider import EmailServiceProvider # Assuming this exists based on step 4
from email_templates import EmailTemplates

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize API clients (assuming API keys are set as environment variables)
SUPPORT_PLATFORM_API_KEY = os.environ.get("SUPPORT_PLATFORM_API_KEY")
EMAIL_SERVICE_API_KEY = os.environ.get("EMAIL_SERVICE_API_KEY")

if not SUPPORT_PLATFORM_API_KEY or not EMAIL_SERVICE_API_KEY:
    logging.error("Missing API keys. Please set SUPPORT_PLATFORM_API_KEY and EMAIL_SERVICE_API_KEY environment variables.")
    exit(1)

support_platform_api = SupportPlatformAPI(api_key=SUPPORT_PLATFORM_API_KEY)
email_service_provider = EmailServiceProvider(api_key=EMAIL_SERVICE_API_KEY)
email_templates = EmailTemplates() # Initializes with predefined templates


@app.route("/webhook/new_inquiry", methods=["POST"])
def new_inquiry_webhook():
    """
    Webhook endpoint to receive new inquiry notifications from the customer support platform.
    """
    try:
        data = request.json
        if not data:
            raise ValueError("No JSON data received in webhook.")

        logging.info(f"Received new inquiry: {json.dumps(data)}")

        inquiry_id = data.get("id")
        inquiry_subject = data.get("subject", "")
        inquiry_description = data.get("description", "")
        customer_email = data.get("customer_email")

        if not customer_email:
            logging.warning(f"Inquiry {inquiry_id} has no customer email. Skipping automated response.")
            return jsonify({"status": "skipped", "message": "No customer email provided."}), 200

        # Step 3: Parse incoming inquiries and categorize
        inquiry_type = categorize_inquiry(inquiry_subject, inquiry_description)

        if inquiry_type:
            template_name = get_template_for_inquiry_type(inquiry_type)
            if template_name:
                email_subject = email_templates.get_template_subject(template_name)
                email_body = email_templates.get_template_body(template_name).format(
                    customer_name=data.get("customer_name", "Customer"),
                    inquiry_id=inquiry_id,
                    inquiry_subject=inquiry_subject
                )

                logging.info(f"Sending automated email for inquiry {inquiry_id} of type '{inquiry_type}'.")
                email_service_provider.send_email(
                    to_email=customer_email,
                    subject=email_subject,
                    body=email_body
                )
                return jsonify({"status": "success", "message": "Automated email sent."}), 200
            else:
                logging.info(f"No email template found for inquiry type '{inquiry_type}'. Skipping automated response.")
        else:
            logging.info(f"Inquiry {inquiry_id} could not be categorized. Skipping automated response.")

        return jsonify({"status": "no_action", "message": "No automated email sent."}), 200

    except ValueError as e:
        logging.error(f"Webhook ValueError: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        logging.error(f"Webhook processing error: {e}", exc_info=True)
        return jsonify({"status": "error", "message": "Internal server error."}), 500

def categorize_inquiry(subject: str, description: str) -> str | None:
    """
    Categorizes an inquiry based on its subject and description.
    This is a simplified example; a real-world scenario would use more advanced NLP/ML.
    """
    text = (subject + " " + description).lower()

    if "password reset" in text or "login issue" in text:
        return "password_reset"
    elif "billing" in text or "invoice" in text or "payment" in text:
        return "billing_inquiry"
    elif "delivery" in text or "shipping" in text or "order status" in text:
        return "order_status"
    elif "product feature" in text or "new feature" in text or "suggestion" in text:
        return "feature_request"
    else:
        return None

def get_template_for_inquiry_type(inquiry_type: str) -> str | None:
    """
    Maps an inquiry type to a specific email template name.
    """
    mapping = {
        "password_reset": "password_reset_confirmation",
        "billing_inquiry": "billing_acknowledgement",
        "order_status": "order_status_acknowledgement",
        "feature_request": "feature_request_acknowledgement"
    }
    return mapping.get(inquiry_type)

if __name__ == "__main__":
    # For local development, use a development server.
    # In production, use a WSGI server like Gunicorn.
    app.run(debug=True, host="0.0.0.0", port=5000)
