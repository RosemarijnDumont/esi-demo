from backend.app.models import db, DashboardData, ReportData
from sqlalchemy import text

def get_dashboard_data(user_id):
    # Optimized query with indexing considerations at DB level
    # Assuming DashboardData is a model that maps to an optimized view or table
    data = db.session.query(DashboardData).filter_by(user_id=user_id).first()
    return data.serialize() if data else {}

def get_report_data(report_id, user_id):
    # Example of a more complex report query that might benefit from specific indexes
    # and query optimization or even a materialized view.
    # This is a placeholder and would be replaced with actual complex report logic.
    sql_query = text("""
        SELECT * FROM report_data 
        WHERE report_id = :report_id AND user_id = :user_id
        -- Further joins and aggregations would go here
    """)
    result = db.session.execute(sql_query, {'report_id': report_id, 'user_id': user_id}).fetchone()
    
    # For actual implementation, map result to a dictionary or object
    if result:
        # Assuming result is a RowProxy or similar, convert to dict
        return dict(result)
    return {}
