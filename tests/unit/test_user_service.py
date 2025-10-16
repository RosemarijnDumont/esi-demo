
import pytest
from unittest.mock import MagicMock
from app.services.user_service import create_user
from app.models.user import User

def test_create_user_success():
    mock_db = MagicMock()
    user_data = {"name": "Test User", "email": "test@example.com", "role": "user"}
    user = create_user(mock_db, user_data)

    assert isinstance(user, User)
    assert user.name == "Test User"
    assert user.email == "test@example.com"
    assert user.role == "user"
    mock_db.add.assert_called_once_with(user)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(user)

def test_create_user_duplicate_email():
    mock_db = MagicMock()
    mock_db.add.side_effect = Exception("Duplicate email") # Simulate a database error
    user_data = {"name": "Test User", "email": "existing@example.com", "role": "user"}

    with pytest.raises(Exception, match="Duplicate email"):
        create_user(mock_db, user_data)

    mock_db.rollback.assert_called_once()

def test_create_user_invalid_role():
    mock_db = MagicMock()
    user_data = {"name": "Test User", "email": "test@example.com", "role": "invalid_role"}

    with pytest.raises(ValueError, match="Invalid role"):
        create_user(mock_db, user_data)

    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()
    mock_db.rollback.assert_not_called()

def test_create_user_missing_data():
    mock_db = MagicMock()
    user_data = {"email": "test@example.com", "role": "user"}

    with pytest.raises(ValueError, match="Missing user data fields"):
        create_user(mock_db, user_data)

    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()
    mock_db.rollback.assert_not_called()
