import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.main import app
from backend.app.db.base import Base
from backend.app.db.session import get_db

# Setup for test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="db_session")
def db_session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def client_fixture(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_create_email_template(client):
    response = client.post(
        "/email-automation/templates/",
        json={
            "name": "Welcome Email",
            "subject": "Welcome, {{ customer_name }}!",
            "body": "Hello {{ customer_name }}, thank you for contacting us."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Welcome Email"
    assert "id" in data

def test_read_email_templates(client):
    client.post(
        "/email-automation/templates/",
        json={
            "name": "Followup Email",
            "subject": "Regarding your ticket",
            "body": "Esteemed customer, your ticket #{{ ticket_id }} has been updated."
        }
    )
    response = client.get("/email-automation/templates/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_create_automation_rule(client):
    template_response = client.post(
        "/email-automation/templates/",
        json={
            "name": "Ticket Closed Template",
            "subject": "Your Ticket {{ ticket_id }} is Closed",
            "body": "Dear {{ customer_name }}, your ticket {{ ticket_id }} has been closed."
        }
    )
    template_id = template_response.json()["id"]

    rule_response = client.post(
        "/email-automation/rules/",
        json={
            "name": "Close Ticket Rule",
            "trigger_event": "ticket_status_change",
            "condition_json": "{\"new_status\": \"Closed\"}",
            "template_id": template_id,
            "is_active": True
        }
    )
    assert rule_response.status_code == 200
    data = rule_response.json()
    assert data["name"] == "Close Ticket Rule"
    assert data["template_id"] == template_id

def test_read_automation_rule(client):
    template_response = client.post(
        "/email-automation/templates/",
        json={
            "name": "Escalated Ticket Template",
            "subject": "Your Ticket {{ ticket_id }} is Escalated",
            "body": "Dear {{ customer_name }}, your ticket {{ ticket_id }} has been escalated."
        }
    )
    template_id = template_response.json()["id"]

    rule_response = client.post(
        "/email-automation/rules/",
        json={
            "name": "Escalate Ticket Rule",
            "trigger_event": "ticket_priority_change",
            "condition_json": "{\"new_priority\": \"High\"}",
            "template_id": template_id,
            "is_active": True
        }
    )
    rule_id = rule_response.json()["id"]

    fetch_response = client.get(f"/email-automation/rules/{rule_id}/")
    assert fetch_response.status_code == 200
    data = fetch_response.json()
    assert data["name"] == "Escalate Ticket Rule"
    assert data["id"] == rule_id


def test_update_email_template(client):
    template_response = client.post(
        "/email-automation/templates/",
        json={
            "name": "Old Template Name",
            "subject": "Old Subject",
            "body": "Old Body Content"
        }
    )
    template_id = template_response.json()["id"]

    update_response = client.put(
        f"/email-automation/templates/{template_id}/",
        json={
            "name": "New Template Name",
            "subject": "New Subject Line",
            "body": "Updated Body Content Here."
        }
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "New Template Name"
    assert data["subject"] == "New Subject Line"
    assert data["body"] == "Updated Body Content Here."

def test_delete_email_template(client):
    template_response = client.post(
        "/email-automation/templates/",
        json={
            "name": "Template to Delete",
            "subject": "Subject to Delete",
            "body": "Body to Delete"
        }
    )
    template_id = template_response.json()["id"]

    delete_response = client.delete(f"/email-automation/templates/{template_id}/")
    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == template_id

    get_response = client.get(f"/email-automation/templates/{template_id}/")
    assert get_response.status_code == 404

def test_update_automation_rule(client):
    # First create a template
    template_response = client.post(
        "/email-automation/templates/",
        json={
            "name": "Generic Template",
            "subject": "Hello from system",
            "body": "Hi there, this is a generic email."
        }
    )
    template_id = template_response.json()["id"]

    # Then create a rule
    rule_response = client.post(
        "/email-automation/rules/",
        json={
            "name": "Initial Rule",
            "trigger_event": "ticket_created",
            "condition_json": "{\"ticket_type\": \"Bug\"}",
            "template_id": template_id,
            "is_active": True
        }
    )
    rule_id = rule_response.json()["id"]

    # Update the rule
    update_response = client.put(
        f"/email-automation/rules/{rule_id}/",
        json={
            "name": "Updated Rule Name",
            "trigger_event": "ticket_updated",
            "condition_json": "{\"ticket_type\": \"Feature Request\"}",
            "is_active": False
        }
    )

    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["name"] == "Updated Rule Name"
    assert updated_data["trigger_event"] == "ticket_updated"
    assert updated_data["is_active"] == False

def test_delete_automation_rule(client):
    template_response = client.post(
        "/email-automation/templates/",
        json={
            "name": "Template For Rule To Delete",
            "subject": "Subject for deletion rule",
            "body": "Body for deletion rule"
        }
    )
    template_id = template_response.json()["id"]

    rule_response = client.post(
        "/email-automation/rules/",
        json={
            "name": "Rule to Delete",
            "trigger_event": "ticket_resolved",
            "template_id": template_id,
            "is_active": True
        }
    )
    rule_id = rule_response.json()["id"]

    delete_response = client.delete(f"/email-automation/rules/{rule_id}/")
    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == rule_id

    get_response = client.get(f"/email-automation/rules/{rule_id}/")
    assert get_response.status_code == 404


# Test rule evaluation and email triggering
def test_rule_evaluation_service_trigger(client, monkeypatch):
    # Mock the email service to prevent actual email sending during tests
    mock_sent_emails = []

    class MockEmailService:
        def send_templated_email(self, template_id, recipient_email, context, automation_rule_id):
            mock_sent_emails.append({
                "template_id": template_id,
                "recipient_email": recipient_email,
                "context": context,
                "automation_rule_id": automation_rule_id
            })
            return {"status": "SIMULATED", "error_message": None}

    monkeypatch.setattr("backend.app.services.email_service.email_service", MockEmailService())

    # Create a template
    template_response = client.post(
        "/email-automation/templates/",
        json={
            "name": "Status Change Template",
            "subject": "Ticket {{ ticket_id }} Status: {{ new_status }}",
            "body": "Dear {{ customer_name }}, your ticket #{{ ticket_id }} is now {{ new_status }}."
        }
    )
    template_id = template_response.json()["id"]

    # Create an automation rule that triggers on ticket status change to 'Closed'
    client.post(
        "/email-automation/rules/",
        json={
            "name": "Ticket Closed Notification",
            "trigger_event": "ticket_status_change",
            "condition_json": "{\"new_status\": \"Closed\"}",
            "template_id": template_id,
            "is_active": True
        }
    )

    from backend.app.services.rule_evaluation_service import rules_evaluation_service

    # Simulate a ticket status change event that should trigger the email
    event_data = {
        "ticket_id": 123,
        "customer_name": "John Doe",
        "recipient_email": "john.doe@example.com",
        "old_status": "Open",
        "new_status": "Closed"
    }
    rules_evaluation_service.evaluate_and_trigger_rules("ticket_status_change", event_data)

    assert len(mock_sent_emails) == 1
    assert mock_sent_emails[0]["recipient_email"] == "john.doe@example.com"
    assert mock_sent_emails[0]["template_id"] == template_id
    assert mock_sent_emails[0]["context"]["ticket_id"] == 123
    assert mock_sent_emails[0]["context"]["new_status"] == "Closed"


def test_rule_evaluation_service_no_trigger_on_condition_fail(client, monkeypatch):
    # Mock the email service to ensure no emails are sent
    mock_sent_emails = []

    class MockEmailService:
        def send_templated_email(self, template_id, recipient_email, context, automation_rule_id):
            mock_sent_emails.append({
                "template_id": template_id,
                "recipient_email": recipient_email,
                "context": context,
                "automation_rule_id": automation_rule_id
            })
            return {"status": "SIMULATED", "error_message": None}

    monkeypatch.setattr("backend.app.services.email_service.email_service", MockEmailService())

    # Create a template
    template_response = client.post(
        "/email-automation/templates/",
        json={
            "name": "Escalation Template",
            "subject": "Ticket {{ ticket_id }} Escalated!",
            "body": "Dear {{ customer_name }}, your ticket #{{ ticket_id }} has been escalated to {{ new_priority }}"
        }
    )
    template_id = template_response.json()["id"]

    # Create an automation rule that triggers on ticket priority change to 'High'
    client.post(
        "/email-automation/rules/",
        json={
            "name": "Ticket Escalation Notification",
            "trigger_event": "ticket_priority_change",
            "condition_json": "{\"new_priority\": \"High\"}",
            "template_id": template_id,
            "is_active": True
        }
    )

    from backend.app.services.rule_evaluation_service import rules_evaluation_service

    # Simulate a ticket priority change event that should NOT trigger the email (priority is Medium)
    event_data = {
        "ticket_id": 456,
        "customer_name": "Jane Doe",
        "recipient_email": "jane.doe@example.com",
        "old_priority": "Low",
        "new_priority": "Medium"
    }
    rules_evaluation_service.evaluate_and_trigger_rules("ticket_priority_change", event_data)

    assert len(mock_sent_emails) == 0

def test_email_logging(client, monkeypatch):
    # Mock SendGrid to simulate success or failure without actual API calls
    class MockSendGridAPIClient:
        def __init__(self, api_key):
            pass

        def send(self, message):
            class MockResponse:
                status_code = 202
                body = b'{"message": "success"}'
            return MockResponse()

    monkeypatch.setattr("backend.app.services.email_service.SendGridAPIClient", MockSendGridAPIClient)
    monkeypatch.setattr("os.getenv", lambda key, default=None: "mock_sendgrid_key" if key == "SENDGRID_API_KEY" else default)

    # Create a template
    template_response = client.post(
        "/email-automation/templates/",
        json={
            "name": "Test Log Template",
            "subject": "Test Log Subject",
            "body": "This is a test log body."
        }
    )
    template_id = template_response.json()["id"]

    from backend.app.services.email_service import email_service
    email_service.send_templated_email(
        template_id=template_id,
        recipient_email="test_log@example.com",
        context={}
    )

    # Verify that an email log entry was created
    response = client.get("/email-automation/email-logs/") # Assuming an endpoint for logs will be added or accessed directly
    assert response.status_code == 200
    logs = response.json()
    sent_log = next((log for log in logs if log["recipient_email"] == "test_log@example.com"), None)
    assert sent_log is not None
    assert sent_log["subject"] == "Test Log Subject"
    assert sent_log["status"] == "SENT"
    assert sent_log["template_id"] == template_id


def test_email_logging_failure(client, monkeypatch):
    # Mock SendGrid to simulate a failure
    class MockSendGridAPIClientFailure:
        def __init__(self, api_key):
            pass

        def send(self, message):
            raise Exception("Simulated SendGrid error")

    monkeypatch.setattr("backend.app.services.email_service.SendGridAPIClient", MockSendGridAPIClientFailure)
    monkeypatch.setattr("os.getenv", lambda key, default=None: "mock_sendgrid_key" if key == "SENDGRID_API_KEY" else default)


    # Create a template
    template_response = client.post(
        "/email-automation/templates/",
        json={
            "name": "Test Log Template Failure",
            "subject": "Test Log Subject Failure",
            "body": "This is a test log body for failure."
        }
    )
    template_id = template_response.json()["id"]

    from backend.app.services.email_service import email_service
    email_service.send_templated_email(
        template_id=template_id,
        recipient_email="test_log_failure@example.com",
        context={}
    )

    # Verify that an email log entry was created with FAILED status
    response = client.get("/email-automation/email-logs/")
    assert response.status_code == 200
    logs = response.json()
    failed_log = next((log for log in logs if log["recipient_email"] == "test_log_failure@example.com"), None)
    assert failed_log is not None
    assert failed_log["subject"] == "Test Log Subject Failure"
    assert failed_log["status"] == "FAILED"
    assert "Simulated SendGrid error" in failed_log["error_message"]
