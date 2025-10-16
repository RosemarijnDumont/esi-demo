
import pytest
from app.services.data_sync import DataSyncService
from app.models.entry import Entry

@pytest.fixture
def data_sync_service():
    return DataSyncService()

def test_mobile_to_web_sync(data_sync_service):
    mobile_entry = {"user_id": 1, "content": "New entry from mobile"}
    synced_entry = data_sync_service.sync_mobile_entry(mobile_entry)
    assert isinstance(synced_entry, Entry)
    assert synced_entry.content == mobile_entry["content"]
    # Further assertions to check if it's visible in web app (mock web app interaction)

def test_realtime_sync_notification(data_sync_service, mocker):
    # Mock a mechanism for web app to receive notifications
    mock_websocket_send = mocker.patch("app.services.data_sync.websocket_manager.send_personal_message")
    mobile_entry = {"user_id": 1, "content": "Another entry"}
    data_sync_service.sync_mobile_entry(mobile_entry)
    mock_websocket_send.assert_called_once_with(1, "New entry available")
