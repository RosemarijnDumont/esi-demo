from flask import Blueprint, jsonify, request
from backend.app.services.report_service import get_dashboard_data, get_report_data
from backend.app.utils.cache import cache

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/dashboard', methods=['GET'])
@cache.cached(timeout=300)  # Cache for 5 minutes
def dashboard():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    data = get_dashboard_data(user_id)
    return jsonify(data)

@reports_bp.route('/report/<report_id>', methods=['GET'])
@cache.cached(timeout=300, query_string=True)  # Cache for 5 minutes, varying by query string
def report(report_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    data = get_report_data(report_id, user_id)
    return jsonify(data)