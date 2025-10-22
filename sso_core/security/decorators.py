
from functools import wraps
from flask import request, jsonify
from sso_core.models.account import Account, AccountType

# Mock user object for demonstration. In a real app, this would come from a JWT or session.
class MockUser:
    def __init__(self, account_id, role):
        self.account_id = account_id
        self.role = role

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # This is a simplified authentication check.
        # In a real application, this would involve token validation (JWT, OAuth etc.)
        # and fetching the authenticated user's details.
        mock_account_id = request.headers.get('X-Account-Id')
        if not mock_account_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        account = Account.get_by_id(mock_account_id)
        if not account:
             return jsonify({'error': 'Invalid account ID'}), 401

        request.user = MockUser(account.id, account.account_type)
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles: list[AccountType]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'user') or request.user.role not in roles:
                return jsonify({'error': 'Unauthorized - Insufficient role permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
