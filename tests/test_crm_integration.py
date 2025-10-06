import unittest
from unittest.mock import patch, Mock
from integrations.crm_integration import CRMIntegration

class TestCRMIntegration(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://mockcrm.com"
        self.api_key = "test_key"
        self.crm = CRMIntegration(self.base_url, self.api_key)

    @patch('requests.post')
    def test_create_ticket_success(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"ticket_id": "123", "status": "new"}
        mock_post.return_value = mock_response

        result = self.crm.create_ticket("test@example.com", "Issue", "Description")
        self.assertIsNotNone(result)
        self.assertEqual(result["ticket_id"], "123")
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_create_ticket_failure(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Network error")
        result = self.crm.create_ticket("test@example.com", "Issue", "Description")
        self.assertIsNone(result)
        mock_post.assert_called_once()

    @patch('requests.put')
    def test_update_ticket_status_success(self, mock_put):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"ticket_id": "123", "status": "closed"}
        mock_put.return_value = mock_response

        result = self.crm.update_ticket_status("123", "closed")
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "closed")
        mock_put.assert_called_once()

    @patch('requests.put')
    def test_update_ticket_status_failure(self, mock_put):
        mock_put.side_effect = requests.exceptions.RequestException("API error")
        result = self.crm.update_ticket_status("123", "closed")
        self.assertIsNone(result)
        mock_put.assert_called_once()

    @patch('requests.get')
    def test_search_tickets_success(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [{"ticket_id": "123", "subject": "Test"}]
        mock_get.return_value = mock_response

        result = self.crm.search_tickets({"status": "open"})
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_search_tickets_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Search error")
        result = self.crm.search_tickets({"status": "open"})
        self.assertIsNone(result)
        mock_get.assert_called_once()
