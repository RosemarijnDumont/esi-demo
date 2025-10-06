import unittest
from unittest.mock import patch, Mock, mock_open
import json
import os

from automations.email_automation_service import EmailAutomationService
from integrations.crm_integration import CRMIntegration
from integrations.email_service_integration import EmailServiceIntegration

class TestEmailAutomationService(unittest.TestCase):

    def setUp(self):
        self.mock_crm = Mock(spec=CRMIntegration)
        self.mock_email_service = Mock(spec=EmailServiceIntegration)
        self.config_file = "test_email_rules.json"

        # Ensure a clean config file for each test
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

        # Create a default configuration for testing
        self.default_rules = {
            "rules": [
                {
                    "scenario": "Password Reset",
                    "subject_keywords": ["password", "reset"],
                    "body_keywords": ["lost access"],
                    "template_id": "template_password_reset",
                    "crm_status_to_update": "pending_reset"
                }
            ]
        }
        with open(self.config_file, "w") as f:
            json.dump(self.default_rules, f)

        self.email_automation = EmailAutomationService(
            self.mock_crm,
            self.mock_email_service,
            config_file=self.config_file
        )

    def tearDown(self):
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def test_load_email_rules_initial(self):
        # Test if rules are loaded correctly at initialization
        self.assertEqual(len(self.email_automation.email_rules["rules"]), 1)
        self.assertEqual(self.email_automation.email_rules["rules"][0]["scenario"], "Password Reset")

    def test_add_email_rule(self):
        new_rule = {
            "scenario": "New Feature Request",
            "subject_keywords": ["feature", "request"],
            "body_keywords": ["suggest", "idea"],
            "template_id": "template_feature_ack",
            "crm_status_to_update": "feature_requested"
        }
        self.email_automation.add_email_rule(
            new_rule["scenario"],
            new_rule["subject_keywords"],
            new_rule["body_keywords"],
            new_rule["template_id"],
            new_rule["crm_status_to_update"]
        )
        self.assertEqual(len(self.email_automation.email_rules["rules"]), 2)
        self.assertEqual(self.email_automation.email_rules["rules"][1]["scenario"], "New Feature Request")

        # Verify it's saved to file
        with open(self.config_file, "r") as f:
            rules_from_file = json.load(f)
            self.assertEqual(len(rules_from_file["rules"]), 2)

    @patch('integrations.email_service_integration.EmailServiceIntegration.get_email_templates')
    @patch('integrations.email_service_integration.EmailServiceIntegration.send_email')
    @patch('integrations.crm_integration.CRMIntegration.update_ticket_status')
    def test_process_incoming_email_match_and_action(self, mock_update_ticket, mock_send_email, mock_get_templates):
        mock_get_templates.return_value = [{
            "id": "template_password_reset",
            "content": "Hello {{customer_email}}, your password reset request has been received."
        }]

        result = self.email_automation.process_incoming_email(
            "customer@example.com",
            "I forgot my password",
            "I lost access to my account, please reset.",
            "TICKET_456"
        )

        self.assertTrue(result)
        mock_send_email.assert_called_once_with(
            to_email="customer@example.com",
            subject="Re: I forgot my password",
            body="Hello customer@example.com, your password reset request has been received.",
            template_id="template_password_reset",
            template_vars={"customer_email": "customer@example.com"}
        )
        mock_update_ticket.assert_called_once_with("TICKET_456", "pending_reset")

    @patch('integrations.email_service_integration.EmailServiceIntegration.get_email_templates')
    @patch('integrations.email_service_integration.EmailServiceIntegration.send_email')
    @patch('integrations.crm_integration.CRMIntegration.update_ticket_status')
    def test_process_incoming_email_no_match(self, mock_update_ticket, mock_send_email, mock_get_templates):
        result = self.email_automation.process_incoming_email(
            "customer@example.com",
            "General inquiry",
            "I have a question about something else."
        )

        self.assertFalse(result)
        mock_send_email.assert_not_called()
        mock_update_ticket.assert_not_called()

    @patch('integrations.email_service_integration.EmailServiceIntegration.get_email_templates')
    @patch('integrations.email_service_integration.EmailServiceIntegration.send_email')
    @patch('integrations.crm_integration.CRMIntegration.update_ticket_status')
    def test_process_incoming_email_no_template_found(self, mock_update_ticket, mock_send_email, mock_get_templates):
        # Mock get_email_templates to return an empty list or no matching template
        mock_get_templates.return_value = []

        result = self.email_automation.process_incoming_email(
            "customer@example.com",
            "I forgot my password",
            "I lost access to my account, please reset.",
            "TICKET_456"
        )

        self.assertTrue(result) # Rule still matches, but email won't be sent
        mock_send_email.assert_not_called() # No email sent because template not found
        mock_update_ticket.assert_called_once() # CRM update should still happen if specified

    def test_update_email_template(self):
        self.mock_email_service.update_email_template.return_value = {"id": "temp_id", "content": "New content"}
        result = self.email_automation.update_email_template("temp_id", "New content")
        self.assertIsNotNone(result)
        self.assertEqual(result["content"], "New content")
        self.mock_email_service.update_email_template.assert_called_once_with("temp_id", "New content")

