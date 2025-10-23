import re

class AutomationRule:
    def __init__(self, rule_id, keywords, inquiry_type, email_template_id, confidence_threshold=0.7):
        self.rule_id = rule_id
        self.keywords = [kw.lower() for kw in keywords]
        self.inquiry_type = inquiry_type
        self.email_template_id = email_template_id
        self.confidence_threshold = confidence_threshold

    def evaluate(self, inquiry_text):
        inquiry_text_lower = inquiry_text.lower()
        matched_keywords = [kw for kw in self.keywords if kw in inquiry_text_lower]
        if matched_keywords:
            # Simple confidence score based on keyword density/presence
            confidence = len(matched_keywords) / len(self.keywords) if self.keywords else 0
            return confidence >= self.confidence_threshold, self.inquiry_type, self.email_template_id, confidence
        return False, None, None, 0

class RuleEngine:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        if not isinstance(rule, AutomationRule):
            raise ValueError("Rule must be an instance of AutomationRule")
        self.rules.append(rule)

    def evaluate_inquiry(self, inquiry_text):
        # Sort rules by number of keywords (more specific rules first)
        sorted_rules = sorted(self.rules, key=lambda rule: len(rule.keywords), reverse=True)

        for rule in sorted_rules:
            is_match, inquiry_type, email_template_id, confidence = rule.evaluate(inquiry_text)
            if is_match:
                return inquiry_type, email_template_id, confidence
        return None, None, 0

# Predefined rules for demonstration
def get_predefined_rules():
    rules = [
        AutomationRule("rule_1", ["password reset", "forgot password"], "password_reset", "template_password_reset"),
        AutomationRule("rule_2", ["billing issue", "invoice", "payment problem"], "billing_inquiry", "template_billing_issue"),
        AutomationRule("rule_3", ["product feature", "new feature request"], "feature_request", "template_feature_request"),
        AutomationRule("rule_4", ["shipping status", "delivery time", "where is my order"], "shipping_inquiry", "template_shipping_status"),
        AutomationRule("rule_5", ["return item", "refund request"], "return_refund", "template_return_refund"),
    ]
    return rules
