
import pytest
from app.services.csv_parser import parse_csv_data

def test_parse_valid_csv():
    csv_content = "name,email,role\nJohn Doe,john@example.com,user\nJane Smith,jane@example.com,admin"
    users = parse_csv_data(csv_content)
    assert len(users) == 2
    assert users[0] == {"name": "John Doe", "email": "john@example.com", "role": "user"}
    assert users[1] == {"name": "Jane Smith", "email": "jane@example.com", "role": "admin"}

def test_parse_csv_with_missing_columns():
    csv_content = "email,role\n無い,john@example.com,user"
    with pytest.raises(ValueError, match="Missing required column: name"):
        parse_csv_data(csv_content)

def test_parse_csv_with_empty_fields():
    csv_content = "name,email,role\nJohn Doe,,user"
    users = parse_csv_data(csv_content)
    assert len(users) == 1
    assert users[0] == {"name": "John Doe", "email": "", "role": "user"}

def test_parse_csv_with_extra_columns():
    csv_content = "name,email,role,extra\nJohn Doe,john@example.com,user,some_data"
    users = parse_csv_data(csv_content)
    assert len(users) == 1
    assert users[0] == {"name": "John Doe", "email": "john@example.com", "role": "user"}

def test_parse_empty_csv():
    csv_content = "name,email,role\n"
    users = parse_csv_data(csv_content)
    assert len(users) == 0

def test_parse_csv_with_invalid_format():
    csv_content = "name,email,role\nJohn Doe,john@example.com\nJane Smith,jane@example.com,admin"
    with pytest.raises(ValueError, match="CSV row has incorrect number of columns"):
        parse_csv_data(csv_content)

