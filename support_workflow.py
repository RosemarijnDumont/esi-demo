import time
from automation_rules import RuleEngine, get_predefined_rules
from nlp_module import NLPModule
from email_templates import EmailTemplateManager, get_predefined_templates
from throttling import ThrottlingMechanism

class SupportWorkflow:
    def __init__(self, confidence_threshold_for_human_review=0.5):
        self.rule_engine = RuleEngine()
        for rule in get_predefined_rules():
            self.rule_engine.add_rule(rule)

        self.nlp_module = NLPModule()

        self.email_template_manager = EmailTemplateManager()
        for template in get_predefined_templates():
            self.email_template_manager.add_template(template)

        self.throttling_mechanism = ThrottlingMechanism()
        self.confidence_threshold_for_human_review = confidence_threshold_for_human_review

    def process_customer_inquiry(self, customer_id, inquiry_text, customer_name, inquiry_details, custom_data=None):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Processing inquiry from customer {customer_id}.")
        processed_text = self.nlp_module.process_inquiry(inquiry_text)
        inquiry_type, template_id, confidence = self.rule_engine.evaluate_inquiry(processed_text)

        personalization_data = {
            "customer_name": customer_name,
            "inquiry_details": inquiry_details,
            ** (custom_data if custom_data else {})
        }

        if inquiry_type and template_id:
            if confidence < self.confidence_threshold_for_human_review:
                print(f"Confidence ({confidence:.2f}) below threshold. Flagging for human review.")
                template_id = "template_human_review_required"
                # Ensure personalization data for human review template is available
                if "inquiry_details" not in personalization_data:
                    personalization_data["inquiry_details"] = inquiry_text[:100] + "..." if len(inquiry_text) > 100 else inquiry_text
            
            if self.throttling_mechanism.can_send_email(customer_id, inquiry_type):
                email_template = self.email_template_manager.get_template(template_id)
                if email_template:
                    subject, body = email_template.render(personalization_data)
                    # In a real system, this would integrate with an email sending service
                    print(f"Sending automated email to {customer_name} ({customer_id}):\nSubject: {subject}\nBody: {body[:200]}...")
                    return {"status": "email_sent", "subject": subject, "body": body, "inquiry_type": inquiry_type, "confidence": confidence}
                else:
                    print(f"Error: Email template '{template_id}' not found. Flagging for human review.")
                    # Fallback to human review if template not found
                    human_review_template = self.email_template_manager.get_template("template_human_review_required")
                    if human_review_template:
                        subject, body = human_review_template.render(personalization_data)
                        print(f"Sending human review fallback email to {customer_name} ({customer_id}):\nSubject: {subject}\nBody: {body[:200]}...")
                        return {"status": "human_review_fallback_email_sent", "subject": subject, "body": body, "inquiry_type": "human_review", "confidence": confidence}
                    return {"status": "error", "message": "Email template not found and no human review fallback.", "confidence": confidence}
            else:
                print(f"Email throttled for customer {customer_id} on inquiry type '{inquiry_type}'.")
                return {"status": "throttled", "inquiry_type": inquiry_type, "confidence": confidence}
        else:
            print(f"No suitable automation rule found for inquiry. Flagging for human review.")
            # If no rule matches, default to human review
            human_review_template = self.email_template_manager.get_template("template_human_review_required")
            if human_review_template:
                subject, body = human_review_template.render(personalization_data)
                print(f"Sending human review email to {customer_name} ({customer_id}):\nSubject: {subject}\nBody: {body[:200]}...")
                return {"status": "human_review_email_sent", "subject": subject, "body": body, "inquiry_type": "human_review", "confidence": confidence}
            return {"status": "error", "message": "No automation rule matched and no human review template.", "confidence": confidence}

# Example Usage
if __name__ == "__main__":
    workflow = SupportWorkflow()

    print("\n--- Test Case 1: Password Reset ---")
    result1 = workflow.process_customer_inquiry(
        customer_id="cust123",
        inquiry_text="I forgot my password, can you help me reset it?",
        customer_name="Alice",
        inquiry_details="password reset",
        custom_data={"reset_link": "https://example.com/reset/123"}
    )
    print(f"Result: {result1}\n")

    print("\n--- Test Case 2: Billing Issue ---")
    result2 = workflow.process_customer_inquiry(
        customer_id="cust456",
        inquiry_text="My last invoice seems incorrect. There's a payment problem.",
        customer_name="Bob",
        inquiry_details="incorrect invoice #XYZ"
    )
    print(f"Result: {result2}\n")

    print("\n--- Test Case 3: Feature Request ---")
    result3 = workflow.process_customer_inquiry(
        customer_id="cust789",
        inquiry_text="I'd like to request a new feature for your product, something about dark mode.",
        customer_name="Charlie",
        inquiry_details="dark mode feature request"
    )
    print(f"Result: {result3}\n")

    print("\n--- Test Case 4: Human Review (Low Confidence) ---")
    result4 = workflow.process_customer_inquiry(
        customer_id="cust101",
        inquiry_text="I have a really specific and unusual question about my advanced settings and some customization options.",
        customer_name="David",
        inquiry_details="unusual advanced settings query",
        custom_data={\