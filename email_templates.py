class EmailTemplate:
    def __init__(self, template_id, subject_template, body_template):
        self.template_id = template_id
        self.subject_template = subject_template
        self.body_template = body_template

    def render(self, personalization_data):
        subject = self.subject_template.format(**personalization_data)
        body = self.body_template.format(**personalization_data)
        return subject, body

class EmailTemplateManager:
    def __init__(self):
        self.templates = {}

    def add_template(self, template):
        if not isinstance(template, EmailTemplate):
            raise ValueError("Template must be an instance of EmailTemplate")
        self.templates[template.template_id] = template

    def get_template(self, template_id):
        return self.templates.get(template_id)

# Predefined email templates for demonstration
def get_predefined_templates():
    templates = [
        EmailTemplate("template_password_reset",
                      "Your Password Reset Request",
                      "Dear {customer_name},\n\nWe received a request to reset your password. Please click on the following link to reset it: {reset_link}\n\nIf you did not request this, please ignore this email.\n\nSincerely,\nThe Support Team"),
        EmailTemplate("template_billing_issue",
                      "Regarding Your Billing Inquiry",
                      "Dear {customer_name},\n\nThank you for reaching out regarding your billing inquiry about {inquiry_details}. Our team is reviewing this and will get back to you within 24 hours.\n\nSincerely,\nThe Support Team"),
        EmailTemplate("template_feature_request",
                      "Thank You for Your Feature Request",
                      "Dear {customer_name},\n\nThank you for your suggestion regarding {inquiry_details}. We appreciate your feedback and will consider it for future updates.\n\nSincerely,\nThe Support Team"),
        EmailTemplate("template_shipping_status",
                      "Your Order Shipping Status",
                      "Dear {customer_name},\n\nYour order {order_number} has been shipped! You can track its status here: {tracking_link}\n\nSincerely,\nThe Support Team"),
        EmailTemplate("template_return_refund",
                      "Regarding Your Return/Refund Request",
                      "Dear {customer_name},\n\nWe have received your request regarding a return/refund for {inquiry_details}. Our team will process this shortly and you will receive a confirmation email.\n\nSincerely,\nThe Support Team"),
        EmailTemplate("template_human_review_required",
                      "Your Inquiry Requires Human Review",
                      "Dear {customer_name},\n\nThank you for your inquiry regarding: {inquiry_details}. We're still working on an automated response for this specific topic, so our human support team will be reviewing your case personally and will get back to you soon.\n\nSincerely,\nThe Support Team"),
    ]
    return templates
