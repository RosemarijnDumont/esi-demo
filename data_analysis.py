import pandas as pd
import re

def analyze_emails(file_path):
    """
    Analyzes a sample of emails currently categorized as 'other' to identify common patterns, keywords,
    and sender/recipient characteristics.

    Args:
        file_path (str): Path to the CSV file containing email data.

    Returns:
        pd.DataFrame: DataFrame with analysis results.
    """
    df = pd.read_csv(file_path)
    other_emails = df[df['category'] == 'other']

    # Basic keyword extraction (can be expanded)
    def extract_keywords(text):
        if isinstance(text, str):
            return list(set(re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())))
        return []

    other_emails['keywords'] = other_emails['subject'].apply(extract_keywords) + \
                               other_emails['body'].apply(extract_keywords)

    print(f"Total 'other' emails: {len(other_emails)}")
    print("\nTop senders in 'other' category:")
    print(other_emails['sender'].value_counts().head(10))
    print("\nMost common keywords in 'other' category:")
    all_keywords = [keyword for sublist in other_emails['keywords'] for keyword in sublist]
    keywords_series = pd.Series(all_keywords)
    print(keywords_series.value_counts().head(20))

    return other_emails

def define_classification_rules():
    """
    Defines clearer, more granular rules for email classification based on identified patterns.
    This function will ideally be updated after collaboration with business stakeholders.
    """
    rules = {
        "priority_request": {
            "keywords": ["urgent", "asap", "immediate", "high priority"],
            "sender_patterns": [".*@company.com"], # Example: emails from within the company
            "subject_patterns": [".*alert.*"]
        },
        "technical_support": {
            "keywords": ["error", "bug", "issue", "login", "password", "technical"],
            "subject_patterns": [".*support.*", ".*problem.*"]
        },
        "billing_inquiry": {
            "keywords": ["invoice", "bill", "payment", "charge", "subscription"],
            "subject_patterns": [".*billing.*", ".*payment.*"]
        },
        "feature_request": {
            "keywords": ["feature", "request", "suggestion", "improve"],
            "body_patterns": [".*would like to see.*", ".*suggestion for.*"]
        },
        "general_inquiry": {
            "keywords": ["question", "inquiry", "information", "hello"],
            "subject_patterns": [".*query.*"]
        },
        "other": {
            "description": "Emails that do not fit into any defined category."
        }
    }
    print("Defined new classification rules:")
    for category, details in rules.items():
        print(f"- {category}: {details.get('description', 'No specific description.')}")
    return rules

def apply_rules_and_tag(email_df, rules):
    """
    Applies the defined classification rules to a DataFrame of emails and tags them.

    Args:
        email_df (pd.DataFrame): DataFrame containing email data with 'subject' and 'body' columns.
        rules (dict): Dictionary of classification rules.

    Returns:
        pd.DataFrame: DataFrame with a new 'predicted_category' column.
    """
    tagged_emails = email_df.copy()
    tagged_emails['predicted_category'] = 'other'

    for index, row in tagged_emails.iterrows():
        text_content = (row['subject'] + " " + (row['body'] if pd.notna(row['body']) else "")).lower()
        for category, rule_details in rules.items():
            if category == 'other':
                continue

            match = False
            # Keyword matching
            if "keywords" in rule_details:
                if any(keyword in text_content for keyword in rule_details["keywords"]):
                    match = True
            # Sender pattern matching
            if "sender_patterns" in rule_details and pd.notna(row['sender']):
                if any(re.match(pattern, row['sender']) for pattern in rule_details["sender_patterns"]):
                    match = True
            # Subject pattern matching
            if "subject_patterns" in rule_details and pd.notna(row['subject']):
                if any(re.match(pattern, row['subject']) for pattern in rule_details["subject_patterns"]):
                    match = True
            # Body pattern matching
            if "body_patterns" in rule_details and pd.notna(row['body']):
                if any(re.search(pattern, row['body']) for pattern in rule_details["body_patterns"]):
                    match = True

            if match:
                tagged_emails.loc[index, 'predicted_category'] = category
                break # Assign the first matching category

    return tagged_emails

def create_refined_dataset(file_path, rules, output_file="refined_email_dataset.csv"):
    """
    Reads an existing email dataset, applies new classification rules, and generates a refined dataset.

    Args:
        file_path (str): Path to the original CSV file containing email data.
        rules (dict): Dictionary of new classification rules.
        output_file (str): Name of the output CSV file for the refined dataset.

    Returns:
        pd.DataFrame: The refined DataFrame.
    """
    df = pd.read_csv(file_path)
    refined_df = apply_rules_and_tag(df, rules)
    refined_df.to_csv(output_file, index=False)
    print(f"Refined dataset created and saved to {output_file}")
    return refined_df

if __name__ == "__main__":
    # Example Usage:

    # 1. Assume 'emails.csv' contains columns like 'sender', 'subject', 'body', 'category'
    #    Create a dummy CSV for demonstration if it doesn't exist
    dummy_data = {
        'sender': ['user1@example.com', 'admin@company.com', 'support@domain.net', 'billing@company.com', 'user2@example.com', 'marketing@example.com', 'ceo@company.com'],
        'subject': ['Question about my account', 'Urgent: Server Down Alert', 'Login issue', 'Your latest bill', 'Feature suggestion', 'New product launch', 'Meeting reminder'],
        'body': ['I have a question about my recent activity.', 'The main server is experiencing an outage. Immediate attention required.', 'I cannot log in to my account. Please help!', 'Please find your bill for this month attached.', 'I would like to suggest a new feature for your software.', 'Check out our exciting new product!', 'Reminder for our meeting tomorrow at 10 AM.'],
        'category': ['other', 'other', 'other', 'other', 'other', 'marketing', 'meeting']
    }
    dummy_df = pd.DataFrame(dummy_data)
    dummy_df.to_csv('emails.csv', index=False)

    # Task 1: Analyze emails
    print("\n--- Analyzing 'other' emails ---")
    analyzed_data = analyze_emails('emails.csv')

    # Task 2 & 3: Define classification rules and tagging schema
    print("\n--- Defining Classification Rules ---")
    new_rules = define_classification_rules()

    # Task 4: Manually categorize and create refined dataset
    print("\n--- Creating Refined Dataset with New Rules ---")
    refined_dataset = create_refined_dataset('emails.csv', new_rules, 'refined_email_dataset.csv')
    print("\nRefined Dataset Head:")
    print(refined_dataset.head())

    print("\nDistribution of New Predicted Categories:")
    print(refined_dataset['predicted_category'].value_counts())
