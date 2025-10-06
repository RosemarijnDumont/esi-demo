from jinja2 import Environment, FileSystemLoader
import os

class RulesEngine:
    def __init__(self, template_dir="email_service/templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.rules = {
            "password_reset": {
                "subject": "Your Password Reset Request",
                "template": "password_reset.html",
                "required_data": ["customer_name", "reset_link"]
            },
            "order_status": {
                "subject": "Your Order Status Update",
                "template": "order_status.html",
                "required_data": ["customer_name", "order_id", "order_status", "tracking_link"]
            },
            "faq_lookup": {
                "subject": "Response to your inquiry",
                "template": "faq_response.html",
                "required_data": ["customer_name", "inquiry_topic", "faq_answer"]
            }
        }

    def get_rule(self, inquiry_type: str):
        return self.rules.get(inquiry_type)

    def render_email(self, inquiry_type: str, data: dict):
        rule = self.get_rule(inquiry_type)
        if not rule:
            return None, None

        template = self.env.get_template(rule["template"])
        rendered_html = template.render(**data)
        return rule["subject"], rendered_html

# Example Usage:
# rules_engine = RulesEngine()
# subject, html = rules_engine.render_email(
#     "password_reset", 
#     {"customer_name": "Alice", "reset_link": "http://example.com/reset/123"}
# )
# print(subject, html)
