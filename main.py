import logging
from email_analysis.model_updater import EmailAnalysisModelUpdater
from email_analysis.model_deployment import EmailAnalysisModelDeployment
import pandas as pd
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_mlops_pipeline(data_path='data/categorized_emails.csv'):
    """
    Orchestrates the entire MLOps pipeline for updating, retraining, validating,
    deploying, and monitoring the email analysis model.
    """
    logging.info("Starting MLOps Pipeline for Email Analysis Model.")

    # Step 1 & 2: Update model with new rules and Retrain
    model_updater = EmailAnalysisModelUpdater(
        model_path='email_analysis_model.joblib',
        vectorizer_path='tfidf_vectorizer.joblib'
    )

    # Check if data file exists, if not, create a dummy one for demonstration
    if not os.path.exists(data_path):
        logging.warning(f"Data file not found at {data_path}. Creating dummy data for demonstration.")
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        dummy_data = {
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
                "I want to close my account.",
                "Important business proposal attached for review.",
                "Request for product catalog and pricing.",
                "Complaint about a recent service interaction.",
                "Technical support query regarding software bug.",
                "Feedback on new website design."
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
                "account_closure",
                "business_proposal",
                "sales_inquiry",
                "customer_complaint",
                "technical_support",
                "website_feedback"
            ]
        }
        pd.DataFrame(dummy_data).to_csv(data_path, index=False)
        logging.info(f"Dummy data created at {data_path}.")

    # Retrain model and perform internal validation
    training_results = model_updater.train_model(data_path=data_path)
    logging.info(f"Model retraining and internal validation complete. Accuracy: {training_results['accuracy']:.4f}")

    # Step 4: Deploy to staging
    model_deployment = EmailAnalysisModelDeployment()
    if model_deployment.deploy_to_staging(
        model_file_path=model_updater.model_path,
        vectorizer_file_path=model_updater.vectorizer_path
    ):
        logging.info("Model successfully deployed to staging.")

        # Step 5: Monitor staging performance
        if model_deployment.monitor_staging_performance(duration_days=7):
            logging.info("Staging monitoring complete and performance criteria met.")

            # Step 6: Promote to production
            if model_deployment.promote_to_production(
                model_file_path=model_updater.model_path,
                vectorizer_file_path=model_updater.vectorizer_path
            ):
                logging.info("Model successfully promoted to production.")

                # Step 6 (continued): Monitor production performance
                model_deployment.monitor_production_performance(duration_days=30)
            else:
                logging.error("Failed to promote model to production.")
        else:
            logging.error("Staging performance monitoring failed or criteria not met. Aborting production promotion.")
    else:
        logging.error("Failed to deploy model to staging. Aborting further steps.")

    logging.info("MLOps Pipeline for Email Analysis Model finished.")

if __name__ == "__main__":
    run_mlops_pipeline()
