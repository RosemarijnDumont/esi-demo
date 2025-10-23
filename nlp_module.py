class NLPModule:
    def __init__(self):
        # In a real-world scenario, this would integrate with a more sophisticated NLP library
        # For this implementation, we rely on the keyword matching in AutomationRule.
        pass

    def process_inquiry(self, inquiry_text):
        # This method can be extended to perform more advanced NLP tasks if needed,
        # such as entity recognition, sentiment analysis, etc.
        # For now, it primarily serves as an interface for the rule engine.
        return inquiry_text # Returning the raw text for keyword matching
