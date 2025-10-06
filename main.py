from integrations.crm_integration import CRMIntegration
from integrations.email_service_integration import EmailServiceIntegration
from automations.email_automation_service import EmailAutomationService
from monitoring.health_check import run_all_health_checks
from monitoring.alerts import trigger_system_health_alert, trigger_email_delivery_alert
import os
import time

# Load configuration from environment variables
CRM_API_BASE_URL = os.getenv("CRM_API_BASE_URL")
CRM_API_KEY = os.getenv("CRM_API_KEY")
EMAIL_SERVICE_API_BASE_URL = os.getenv("EMAIL_SERVICE_API_BASE_URL")
EMAIL_SERVICE_API_KEY = os.getenv("EMAIL_SERVICE_API_KEY")
EMAIL_RULES_CONFIG_FILE = os.getenv("EMAIL_RULES_CONFIG_FILE", "config/email_rules.json")

POLLING_INTERVAL_SECONDS = int(os.getenv("POLLING_INTERVAL_SECONDS", 60)) # How often to check for new emails/tickets

def initialize_services():
    if not all([CRM_API_BASE_URL, CRM_API_KEY, EMAIL_SERVICE_API_BASE_URL, EMAIL_SERVICE_API_KEY]):
        print("ERROR: Missing one or more required environment variables for service initialization.")
        print("Please set CRM_API_BASE_URL, CRM_API_KEY, EMAIL_SERVICE_API_BASE_URL, EMAIL_SERVICE_API_KEY.")
        exit(1)

    crm_integration = CRMIntegration(CRM_API_BASE_URL, CRM_API_KEY)
    email_service_integration = EmailServiceIntegration(EMAIL_SERVICE_API_BASE_URL, EMAIL_SERVICE_API_KEY)
    email_automation_service = EmailAutomationService(crm_integration, email_service_integration, EMAIL_RULES_CONFIG_FILE)
    return crm_integration, email_service_integration, email_automation_service

def simulate_incoming_ticket(crm_integration, email_automation_service, customer_email, subject, body):
    print(f"\n[SIMULATION] Incoming customer email from {customer_email}: '{subject}'")
    # In a real system, this would come from a webhook or polling the CRM/email inbox
    # For this simulation, we'll create a CRM ticket first.
    ticket = crm_integration.create_ticket(customer_email, subject, body)
    if ticket:
        ticket_id = ticket.get("ticket_id")
        print(f"[SIMULATION] CRM ticket created: {ticket_id}")
        processed = email_automation_service.process_incoming_email(customer_email, subject, body, ticket_id)
        if processed:
            print(f"[SIMULATION] Automated email response processed for ticket {ticket_id}.")
        else:
            print(f"[SIMULATION] No automated rule matched for ticket {ticket_id}. Manual review needed.")
    else:
        print("[SIMULATION] Failed to create CRM ticket. No automation could be triggered.")

def main():
    print("Starting Automated Email System...")

    crm_integration, email_service_integration, email_automation_service = initialize_services()

    # Initial health check
    if not run_all_health_checks():
        trigger_system_health_alert("Automated Email System", "One or more core services are down at startup.")
        print("Critical services are down. Exiting.")
        exit(1)

    print(f"System initialized. Polling for new inquiries every {POLLING_INTERVAL_SECONDS} seconds.")

    # Example: Simulate some incoming customer inquiries
    simulate_incoming_ticket(
        crm_integration, email_automation_service,
        "alice@example.com", "My order hasn't arrived", "I made an order last week, but I haven't received any confirmation or shipping updates."
    )
    simulate_incoming_ticket(
        crm_integration, email_automation_service,
        "bob@example.com", "Forgot Password Help", "I need to reset my password, can you help me with that?"
    )
    simulate_incoming_ticket(
        crm_integration, email_automation_service,
        "charlie@example.com", "General Question", "I just have a quick question about your services."
    )

    while True:
        # In a real-world scenario, this loop would regularly poll the CRM/email system
        # for new tickets/emails and feed them to `email_automation_service.process_incoming_email`.
        # For this example, we'll just re-run health checks and wait.
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running routine checks...")
        if not run_all_health_checks():
            trigger_system_health_alert("Automated Email System", "One or more core services became unhealthy during operation.")

        # Example of how you might update templates dynamically (e.g., via an admin panel)
        # email_automation_service.update_email_template("template_password_reset", "Updated password reset instructions.")

        time.sleep(POLLING_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
