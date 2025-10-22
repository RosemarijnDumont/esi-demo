from flask import Blueprint, jsonify, request, current_app
from app.models import db, Report
from app.utils.cache import cache

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports/<int:report_id>', methods=['GET'])
@cache.cached(timeout=60 * 10, key_prefix='report_detail') # Cache for 10 minutes
def get_report_detail(report_id):
    """
    Retrieves a single report's details, utilizing server-side caching.
    """
    current_app.logger.info(f"Fetching report detail for report ID: {report_id}...")
    try:
        report = Report.query.get(report_id)
        if report:
            current_app.logger.info(f"Report {report_id} fetched successfully.")
            return jsonify({'id': report.id, 'title': report.title, 'content': report.content, 'timestamp': report.timestamp.isoformat()}), 200
        current_app.logger.warning(f"Report {report_id} not found.")
        return jsonify({"error": "Report not found"}), 404
    except Exception as e:
        current_app.logger.error(f"Error fetching report {report_id}: {e}")
        return jsonify({"error": "Failed to retrieve report detail"}), 500

@reports_bp.route('/reports/filter', methods=['GET'])
def filter_reports():
    """
    Filters reports based on query parameters, with optimized database query.
    Does *not* cache this endpoint due to dynamic filtering.
    """
    current_app.logger.info("Filtering reports...")
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        search_term = request.args.get('search')

        query = Report.query

        if start_date:
            query = query.filter(Report.timestamp >= start_date)
        if end_date:
            query = query.filter(Report.timestamp <= end_date)
        if search_term:
            query = query.filter(Report.title.ilike(f'%{search_term}%') | Report.content.ilike(f'%{search_term}%'))
        
        # Assuming Report.timestamp and Report.title are indexed
        reports = query.order_by(Report.timestamp.desc()).all()

        reports_data = [{'id': r.id, 'title': r.title, 'content': r.content, 'timestamp': r.timestamp.isoformat()} for r in reports]
        current_app.logger.info(f"{len(reports_data)} reports filtered successfully.")
        return jsonify(reports_data), 200
    except Exception as e:
        current_app.logger.error(f"Error filtering reports: {e}")
        return jsonify({"error": "Failed to filter reports"}), 500
