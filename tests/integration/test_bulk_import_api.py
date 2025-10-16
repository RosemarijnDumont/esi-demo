
import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_bulk_import_success():
    csv_content = "name,email,role\nJohn Doe,john@example.com,user\nJane Smith,jane@example.com,admin"
    files = {"file": ("users.csv", csv_content, "text/csv")}

    with patch("app.services.user_service.create_user") as mock_create_user:
        mock_create_user.return_value = None # We don't need a full User object for this test
        response = client.post("/api/users/bulk-import", files=files)

    assert response.status_code == 200
    assert response.json() == {"message": "Bulk import completed", "imported_count": 2, "errors": []}
    assert mock_create_user.call_count == 2

def test_bulk_import_with_errors():
    csv_content = "name,email,role\nJohn Doe,john@example.com,user\nInvalid User,,invalid_role"
    files = {"file": ("users.csv", csv_content, "text/csv")}

    with patch("app.services.user_service.create_user") as mock_create_user:
        def create_user_side_effect(db, user_data):
            if user_data["name"] == "Invalid User":
                raise ValueError("Invalid role")
            return None
        mock_create_user.side_effect = create_user_side_effect

        response = client.post("/api/users/bulk-import", files=files)

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["message"] == "Bulk import completed with errors"
    assert response_json["imported_count"] == 1
    assert len(response_json["errors"]) == 1
    assert "Invalid role" in response_json["errors"][0]

def test_bulk_import_invalid_file_type():
    files = {"file": ("document.txt", "some content", "text/plain")}
    response = client.post("/api/users/bulk-import", files=files)

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type. Please upload a CSV file."}

def test_bulk_import_empty_file():
    csv_content = ""
    files = {"file": ("empty.csv", csv_content, "text/csv")}
    response = client.post("/api/users/bulk-import", files=files)

    assert response.status_code == 400
    assert response.json() == {"detail": "Uploaded CSV file is empty."}

def test_bulk_import_missing_columns():
    csv_content = "email,role\n無い,john@example.com,user"
    files = {"file": ("users.csv", csv_content, "text/csv")}

    response = client.post("/api/users/bulk-import", files=files)
    assert response.status_code == 400
    assert response.json() == {"detail": "CSV parsing error: Missing required column: name"}

def test_bulk_import_large_file_performance():
    # This is a basic integration test, full performance testing needs dedicated tools
    num_users = 1000
    csv_header = "name,email,role\n"
    csv_rows = [f"User {i},user{i}@example.com,user" for i in range(num_users)]
    csv_content = csv_header + "\n".join(csv_rows)

    files = {"file": ("large_users.csv", csv_content, "text/csv")}

    with patch("app.services.user_service.create_user", return_value=None):  # Mock user creation for speed
        response = client.post("/api/users/bulk-import", files=files)

    assert response.status_code == 200
    assert response.json()["imported_count"] == num_users
    assert not response.json()["errors"]
