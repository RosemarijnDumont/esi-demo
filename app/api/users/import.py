
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import os
import uuid

users_import_bp = Blueprint('users_import', __name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# In-memory staging area for simplicity. In a real app, use a database.
staged_imports = {}

@users_import_bp.route('/api/users/import', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        import_id = str(uuid.uuid4())
        try:
            df = pd.read_csv(filepath)
            # Initial validation: Check if required columns exist (e.g., 'email', 'first_name', 'last_name')
            required_columns = ['email', 'first_name', 'last_name'] # Example required columns
            if not all(col in df.columns for col in required_columns):
                return jsonify({'error': f'Missing required columns. Expected: {', '.join(required_columns)}'}), 400
            
            # Store data in staging area
            staged_imports[import_id] = {
                'filename': filename,
                'status': 'staged',
                'users': df.to_dict(orient='records'),
                'column_mapping': None # To be set by admin later
            }
            return jsonify({'message': 'CSV uploaded and staged successfully', 'import_id': import_id}), 200
        except Exception as e:
            return jsonify({'error': f'Error processing CSV: {str(e)}'}), 500
    return jsonify({'error': 'Invalid file type'}), 400

@users_import_bp.route('/api/users/import/staged', methods=['GET'])
def get_staged_imports():
    return jsonify(staged_imports), 200

@users_import_bp.route('/api/users/import/staged/<string:import_id>', methods=['GET'])
def get_staged_import_details(import_id):
    if import_id not in staged_imports:
        return jsonify({'error': 'Import not found'}), 404
    
    return jsonify(staged_imports[import_id]), 200

@users_import_bp.route('/api/users/import/staged/<string:import_id>', methods=['PUT'])
def update_staged_import(import_id):
    if import_id not in staged_imports:
        return jsonify({'error': 'Import not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Example: Allow updating column mapping or individual user details
    if 'column_mapping' in data:
        staged_imports[import_id]['column_mapping'] = data['column_mapping']
    if 'users' in data:
        staged_imports[import_id]['users'] = data['users']
    
    return jsonify({'message': 'Staged import updated successfully', 'import_id': import_id}), 200

@users_import_bp.route('/api/users/import/activate/<string:import_id>', methods=['PUT'])
def activate_imported_users(import_id):
    if import_id not in staged_imports:
        return jsonify({'error': 'Import not found'}), 404
    
    staged_data = staged_imports[import_id]
    if staged_data['status'] != 'staged':
        return jsonify({'error': 'Import not in staged status'}), 400
    
    # Simulate user creation and role assignment
    successful_users = []
    failed_users = []

    # In a real application, you would iterate through staged_data['users']
    # create actual user accounts in your database, assign default roles/permissions,
    # and handle any business logic. This is a placeholder.
    for user_data in staged_data['users']:
        # Apply column mapping if available
        mapped_user_data = {}
        if staged_data['column_mapping']:
            for csv_col, sys_attr in staged_data['column_mapping'].items():
                if csv_col in user_data:
                    mapped_user_data[sys_attr] = user_data[csv_col]
        else:
            mapped_user_data = user_data # No mapping, use as is

        # Basic validation before 