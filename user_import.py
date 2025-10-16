import csv
from io import StringIO
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

user_import_bp = Blueprint('user_import', __name__)

# In a real application, these would be integrated with actual user management services
def create_user(user_data):
    # Simulate user creation. In a real app, this would interact with a database/ORM.
    print(f"Creating user: {user_data}")
    if user_data.get('email') == 'existing@example.com':
        return False, "User with this email already exists."
    return True, "User created successfully."

@user_import_bp.route('/users/import', methods=['POST'])
def import_users():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Read the CSV content
        csv_data = file.read().decode('utf-8')
        
        successes = []
        failures = []
        
        # Process CSV
        try:
            csvfile = StringIO(csv_data)
            reader = csv.DictReader(csvfile)
            
            required_headers = ['username', 'email', 'first_name', 'last_name', 'roles']
            if not all(header in reader.fieldnames for header in required_headers):
                return jsonify({'message': 'Missing one or more required CSV headers (username, email, first_name, last_name, roles)'}), 400

            for i, row in enumerate(reader):
                row_num = i + 1  # For user-friendly error reporting
                user_data = {
                    'username': row.get('username'),
                    'email': row.get('email'),
                    'first_name': row.get('first_name'),
                    'last_name': row.get('last_name'),
                    'roles': [role.strip() for role in row.get('roles', '').split(',')] if row.get('roles') else []
                }
                
                # Basic validation
                if not all([user_data['username'], user_data['email'], user_data['first_name'], user_data['last_name']]):
                    failures.append({'row': row_num, 'data': row, 'reason': 'Missing required user data fields.'})
                    continue

                # Attempt to create user
                success, message = create_user(user_data)
                if success:
                    successes.append({'row': row_num, 'data': row, 'message': message})
                else:
                    failures.append({'row': row_num, 'data': row, 'reason': message})

        except csv.Error as e:
            return jsonify({'message': f"CSV parsing error: {e}"}), 400
        except Exception as e:
            return jsonify({'message': f"An unexpected error occurred: {e}"}), 500

        return jsonify({
            'message': 'User import complete',
            'summary': {
                'total_rows': len(successes) + len(failures),
                'successful_imports': len(successes),
                'failed_imports': len(failures)
            },
            'details': {
                'successes': successes,
                'failures': failures
            }
        }), 200
    else:
        return jsonify({'message': 'File type not allowed'}), 400

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'csv'}

# Example of how to integrate into a Flask app:
# from flask import Flask
# app = Flask(__name__)
# app.register_blueprint(user_import_bp, url_prefix='/api')

# if __name__ == '__main__':
#     app.run(debug=True)