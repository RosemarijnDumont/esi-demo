import unittest
from unittest.mock import patch, Mock
from integrations.email_service_integration import EmailServiceIntegration

class TestEmailServiceIntegration(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://mockemailservice.com"
        self.api_key = "test_key"
        self.email_service = EmailServiceIntegration(self.base_url, self.api_key)

    @patch('requests.post')
    def test_send_email_success(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"message": "Email sent successfully"}
        mock_post.return_value = mock_response

        result = self.email_service.send_email("test@example.com", "Subject", "Body")
        self.assertIsNotNone(result)
        self.assertEqual(result["message"], "Email sent successfully")
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_send_email_with_template_success(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"message": "Templated email sent successfully"}
        mock_post.return_value = mock_response

        result = self.email_service.send_email("test@example.com", "Subject", "Body", "template_id_1", {"var": "value"})
        self.assertIsNotNone(result)
        self.assertEqual(result["message"], "Templated email sent successfully")
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_send_email_failure(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("SMTP error")
        result = self.email_service.send_email("test@example.com", "Subject", "Body")
        self.assertIsNone(result)
        mock_post.assert_called_once()

    @patch('requests.get')
    def test_get_email_templates_success(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [{"id": "temp1", "name": "Template 1"}]
        mock_get.return_value = mock_response

        result = self.email_service.get_email_templates()
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_get_email_templates_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Fetch error")
        result = self.email_service.get_email_templates()
        self.assertIsNone(result)
        mock_get.assert_called_once()

    @patch('requests.put')
    def test_update_email_template_success(self, mock_put):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"id": "temp1", "content": "New Content"}
        mock_put.return_value = mock_response

        result = self.email_service.update_email_template("temp1", "New Content")
        self.assertIsNotNone(result)
        self.assertEqual(result["content"], "New Content")
        mock_put.assert_called_once()

    @patch('requests.put')
    def test_update_email_template_failure(self, mock_put):
        mock_put.side_effect = requests.exceptions.RequestException("Update error")
        result = self.email_service.update_email_template("temp1", "New Content")
        self.assertIsNone(result)
        mock_put.assert_called_once()
