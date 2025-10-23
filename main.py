# This file acts as an entry point or main application logic
from support_workflow import SupportWorkflow

def initialize_support_system():
    """Initializes and returns the SupportWorkflow instance."""
    return SupportWorkflow()

if __name__ == "__main__":
    # Example of how the system would be used in a larger application
    support_workflow = initialize_support_system()

    # Simulate an incoming customer inquiry from a support platform
    # In a real integration, this data would come from an API webhook or message queue
    print("\n--- Simulating Live Inquiries ---")

    # Inquiry 1: Automated Response (Password Reset)
    support_workflow.process_customer_inquiry(
        customer_id="customer_A",
        inquiry_text="I need to reset my password, can you help me with that?",
        customer_name="Eva",
        inquiry_details="forgot password"
    )

    # Inquiry 2: Automated Response (Billing Issue)
    support_workflow.process_customer_inquiry(
        customer_id="customer_B",
        inquiry_text="My billing statement is incorrect. I have a payment problem.",
        customer_name="Frank",
        inquiry_details="invoice discrepancy"
    )

    # Inquiry 3: Requires Human Review (No direct match)
    support_workflow.process_customer_inquiry(
        customer_id="customer_C",
        inquiry_text="Can you tell me more about your company's long-term vision and sustainability efforts?",
        customer_name="Grace",
        inquiry_details="company vision query"
    )

    # Inquiry 4: Throttled Email (Duplicate Password Reset for same customer within window)
    support_workflow.process_customer_inquiry(
        customer_id="customer_A",
        inquiry_text="Still having issues with my password. Is there another way to reset?",
        customer_name="Eva",
        inquiry_details="second password reset attempt"
    )

    # Inquiry 5: Human Review (Low confidence on something vaguely related to features)
    support_workflow.process_customer_inquiry(
        customer_id="customer_D",
        inquiry_text="What are some of the interesting capabilities that your users enjoy in the new update?",
        customer_name="Heidi",
        inquiry_details="general capabilities question",
        custom_data={"new_feature_info": "improved performance and UI"}
    )

    # Inquiry 6: Automated Response (Shipping Status)
    support_workflow.process_customer_inquiry(
        customer_id="customer_E",
        inquiry_text="Where is my order? What's the shipping status of order #XYZ123?",
        customer_name="Ivan",
        inquiry_details="order #XYZ123 status",
        custom_data={"order_number": "XYZ123", "tracking_link": "https://tracker.example.com/XYZ123"}
    )

    print("\n--- Support system simulation finished ---")
