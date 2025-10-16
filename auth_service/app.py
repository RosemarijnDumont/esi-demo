from flask import Flask, request, jsonify
from auth_service.auth import AuthService

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'super-secret-key-that-should-be-in-env-vars'
auth_service = AuthService(app.config['SECRET_KEY'])

@app.route('/login', methods=['POST'])
def login():
    auth_data = request.get_json()
    username = auth_data.get('username')
    password = auth_data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    try:
        user = auth_service.authenticate_user(username, password)
        if user:
            token = auth_service.generate_token(user['user_id'])
            return jsonify({'token': token.decode('UTF-8')}), 200
        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        app.logger.error(f"Login error for user {username}: {e}")
        return jsonify({'message': 'An error occurred during login.'}), 500

@app.route('/protected', methods=['GET'])
@auth_service.login_required
def protected_route(current_user):
    return jsonify({'message': f'Hello, {current_user}! You accessed a protected route.'}), 200

@app.route('/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({'message': 'Token is missing for refresh'}), 400
    
    try:
        refreshed_data = auth_service.refresh_token(token)
        if 'error' in refreshed_data:
            return jsonify({'message': refreshed_data['error']}), 401
        return jsonify({'token': refreshed_data['token'].decode('UTF-8')}), 200
    except Exception as e:
        app.logger.error(f"Token refresh error: {e}")
        return jsonify({'message': 'An error occurred during token refresh.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
