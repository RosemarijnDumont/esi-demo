from integrations.crm_integration import CRMIntegration
from integrations.email_service_integration import EmailServiceIntegration
import json
import os

class EmailAutomationService:
    def __init__(self, crm_integration: CRMIntegration, email_service_integration: EmailServiceIntegration, config_file="config/email_rules.json"):
        self.crm_integration = crm_integration
        self.email_service_integration = email_service_integration
        self.config_file = config_file
        self.email_rules = self._load_email_rules()

    def _load_email_rules(self):
        if not os.path.exists(self.config_file):
            return {"rules": []}
        with open(self.config_file, "r") as f:
            return json.load(f)

    def _save_email_rules(self):
        with open(self.config_file, "w") as f:
            json.dump(self.email_rules, f, indent=4)

    def add_email_rule(self, scenario, subject_keywords, body_keywords, template_id, crm_status_to_update=None):
        rule = {
            "scenario": scenario,
            "subject_keywords": subject_keywords,
            "body_keywords": body_keywords,
            "template_id": template_id,
            "crm_status_to_update": crm_status_to_update
        }
        self.email_rules["rules"].append(rule)
        self._save_email_rules()

    def process_incoming_email(self, customer_email, subject, body, ticket_id=None):
        for rule in self.email_rules["rules"]:
            subject_match = any(keyword.lower() in subject.lower() for keyword in rule["subject_keywords"])
            body_match = any(keyword.lower() in body.lower() for keyword in rule["body_keywords"])

            if subject_match or body_match:
                # Send automated email
                email_template = self.email_service_integration.get_email_templates()
                template_content = next((t["content"] for t in email_template if t["id"] == rule["template_id"]), None)

                if template_content:
                    # Basic templating, ideally use a more robust templating engine
                    formatted_body = template_content.replace("{{customer_email}}", customer_email)
                    # Add more template variable replacements as needed

                    self.email_service_integration.send_email(
                        to_email=customer_email,
                        subject=f"Re: {subject}",
                        body=formatted_body,
                        template_id=rule["template_id"],
                        template_vars={
                            "customer_email": customer_email,
                            # ... often other variables relevant to a template
                        }
                    )
                    print(f"Automated email sent to {customer_email} for scenario: {rule['scenario']}")

                # Update CRM ticket status if specified
                if ticket_id and rule["crm_status_to_update"]:
                    self.crm_integration.update_ticket_status(ticket_id, rule["crm_status_to_update"])
                    print(f"CRM ticket {ticket_id} status updated to {rule['crm_status_to_update']}")

                return True # Rule matched and processed
        return False # No rule matched

    def update_email_template(self, template_id, new_content):
        return self.email_service_integration.update_email_template(template_id, new_content)

# Example usage in a main application flow:
# from integrations.crm_integration import CRMIntegration
# from integrations.email_service_integration import EmailServiceIntegration

# crm_integration = CRMIntegration("https://api.examplecrm.com", "your_crm_api_key")
# email_service_integration = EmailServiceIntegration("https://api.exampleemailservice.com", "your_email_api_key")
# email_automation = EmailAutomationService(crm_integration, email_service_integration)

# # Add some example rules
# email_automation.add_email_rule(
#     "Password Reset",
#     ["password", "reset", "forgot"],
#     ["reset my password", "lost access"],
#     "template_password_reset", # This should be an ID from your email service
#     "pending_reset"
# )
# email_automation.add_email_rule(
#     "Order Confirmation",
#     ["order", "confirmation"],
#     ["receive my order", "did my order go through"],
#     "template_order_confirmation",
#     "order_confirmed"
# )

# # Simulate an incoming email
# email_automation.process_incoming_email(
#     "customer@example.com",
#     "Forgot my password please help",
#     "I need to reset my password for my account.",
#     "TICKET_123"
# )
