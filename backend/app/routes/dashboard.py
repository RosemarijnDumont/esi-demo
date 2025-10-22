from flask import Blueprint, jsonify, current_app
from app.models import db, Report, Dashboard
from app.utils.cache import cache

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/data', methods=['GET'])
@cache.cached(timeout=60 * 5, key_prefix='dashboard_data') # Cache for 5 minutes
def get_dashboard_data():
    """
    Retrieves dashboard data, optimizing for common queries.
    Implements server-side caching.
    """
    current_app.logger.info("Fetching dashboard data...")
    try:
        # Example: Optimized query with indexing considerations for Report.timestamp
        # Assuming Report.timestamp is indexed for efficient filtering/ordering
        reports = Report.query.order_by(Report.timestamp.desc()).limit(100).all()
        dashboard_widgets = Dashboard.query.all()

        # Serialize data (example, adapt to your actual models)
        reports_data = [{'id': r.id, 'title': r.title, 'content': r.content, 'timestamp': r.timestamp.isoformat()} for r in reports]
        dashboard_widgets_data = [{'id': d.id, 'name': d.name, 'value': d.value} for d in dashboard_widgets]

        current_app.logger.info("Dashboard data fetched successfully.")
        return jsonify({"reports": reports_data, "widgets": dashboard_widgets_data}), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching dashboard data: {e}")
        return jsonify({"error": "Failed to retrieve dashboard data"}), 500
