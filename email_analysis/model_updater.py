import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EmailAnalysisModelUpdater:
    def __init__(self, model_path='email_analysis_model.joblib', vectorizer_path='tfidf_vectorizer.joblib'):
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.model = None
        self.vectorizer = None

    def _define_classification_rules(self, email_content):
        """
        Defines clearer classification rules for email content.
        This is a pre-processing step to help categorize emails before model training.
        """
        email_content = email_content.lower()

        if "invoice" in email_content or "billing statement" in email_content:
            return "billing"
        elif "password reset" in email_content or "account recovery" in email_content:
            return "password_reset"
        elif "delivery status" in email_content or "shipping update" in email_content:
            return "delivery_update"
        elif "meeting request" in email_content or "calendar invite" in email_content:
            return "meeting_request"
        elif "unsubscrib" in email_content or "opt out" in email_content:
            return "unsubscribe_request"
        else:
            # If no specific rule matches, it falls to the model to classify or remains 'other'
            return None  # Indicate that further model classification is needed

    def preprocess_data(self, df):
        """
        Applies the classification rules and prepares data for vectorization.
        """
        logging.info("Applying classification rules and preprocessing data...")
        df['predicted_category_rule'] = df['email_content'].apply(self._define_classification_rules)
        
        # For emails where rules provided a category, use it. Otherwise, keep the original label (potentially 'other').
        # The model will learn to refine these or classify the Nones.
        df['final_category_for_training'] = df.apply(
            lambda row: row['predicted_category_rule'] if row['predicted_category_rule'] is not None else row['category'],
            axis=1
        )
        return df

    def train_model(self, data_path, test_size=0.2, random_state=42):
        """
        Retrains the email analysis model using the refined and categorized dataset.
        """
        logging.info(f"Loading data from {data_path}...")
        df = pd.read_csv(data_path)
        df = self.preprocess_data(df)

        X = df['email_content']
        y = df['final_category_for_training']

        logging.info("Splitting data into training and testing sets...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

        logging.info("Initializing and fitting TF-IDF Vectorizer...")
        self.vectorizer = TfidfVectorizer(max_features=5000)
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)

        logging.info("Initializing and training SVM model...")
        self.model = SVC(kernel='linear', probability=True, random_state=random_state)
        self.model.fit(X_train_vec, y_train)

        logging.info("Performing internal validation and testing...")
        y_pred = self.model.predict(X_test_vec)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        logging.info(f"Model Accuracy: {accuracy:.4f}")
        logging.info(f"\nClassification Report:\n{report}")

        # Save the retrained model and vectorizer
        self._save_model()
        logging.info("Model retraining complete and saved.")
        return {"accuracy": accuracy, "report": report}

    def _save_model(self):
        """
        Saves the trained model and vectorizer to disk.
        """
        logging.info(f"Saving model to {self.model_path} and vectorizer to {self.vectorizer_path}...")
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)

    def load_model(self):
        """
        Loads the trained model and vectorizer from disk.
        """
        logging.info(f"Loading model from {self.model_path} and vectorizer from {self.vectorizer_path}...")
        try:
            self.model = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
            logging.info("Model and vectorizer loaded successfully.")
            return True
        except FileNotFoundError:
            logging.error("Model or vectorizer files not found. Please train the model first.")
            return False

    def predict(self, email_content):
        """
        Makes a prediction for a single email, incorporating the initial classification rules.
        """
        rule_based_category = self._define_classification_rules(email_content)
        if rule_based_category:
            return rule_based_category

        if self.model is None or self.vectorizer is None:
            if not self.load_model():
                return "Error: Model not loaded."

        email_vec = self.vectorizer.transform([email_content])
        prediction = self.model.predict(email_vec)
        return prediction[0]

if __name__ == "__main__":
    # Example Usage:
    # Create a dummy dataset for demonstration
    data = {
        'email_content': [
            "Please find attached the invoice for your last purchase.",
            "I need to reset my password, I forgot it.",
            "Your order has been shipped and is expected to arrive tomorrow.",
            "Can we schedule a meeting next week to discuss the project?",
            "Unsubscribe me from your mailing list, thank you.",
            "This is a generic email with no clear category.",
            "Can you send me the latest sales report?",
            "I have a question about my account, it seems locked.",
            "I'd like to update my personal information.",
            "This is another email that seems generic.",
            "Where is my package? The tracking number is ABC123DEF.",
            "I need assistance with my premium subscription.",
            "Could you provide more details on the upcoming event?",
            "My payment for the invoice is overdue.",
            "I want to close my account."
        ],
        'category': [
            "billing",
            "password_reset",
            "delivery_update",
            "meeting_request",
            "unsubscribe_request",
            "other",
            "report_request",
            "account_issue",
            "account_update",
            "other",
            "delivery_update",
            "subscription_support",
            "event_inquiry",
            "billing",
            "account_closure"
        ]
    }
    dummy_df = pd.DataFrame(data)
    dummy_df.to_csv('dummy_email_data.csv', index=False)

    updater = EmailAnalysisModelUpdater()
    results = updater.train_model('dummy_email_data.csv')
    print(f"Training results: {results}")

    # Test prediction
    new_email = "I need help with my account, can't log in."
    predicted_category = updater.predict(new_email)
    print(f"\nNew email: '{new_email}'\nPredicted category: {predicted_category}")

    new_email_2 = "Where is my order from last week?"
    predicted_category_2 = updater.predict(new_email_2)
    print(f"\nNew email: '{new_email_2}'\nPredicted category: {predicted_category_2}")

    new_email_3 = "This is a very generic email asking for no specific service."
    predicted_category_3 = updater.predict(new_email_3)
    print(f"\nNew email: '{new_email_3}'\nPredicted category: {predicted_category_3}")

    new_email_4 = "Please approve the attached budget for next quarter."
    predicted_category_4 = updater.predict(new_email_4)
    print(f"\nNew email: '{new_email_4}'\nPredicted category: {predicted_category_4}")

    new_email_5 = "I would like to unsubscribe from marketing emails."
    predicted_category_5 = updater.predict(new_email_5)
    print(f"\nNew email: '{new_email_5}'\nPredicted category: {predicted_category_5}")