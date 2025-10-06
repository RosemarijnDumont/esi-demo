from backend.app.__init__ import db

# Placeholder for optimized dashboard data representation
# In a real scenario, this might be a view or a denormalized table for performance.
class DashboardData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False, index=True)
    data = db.Column(db.JSON) # Store pre-aggregated or frequently accessed data as JSON

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'data': self.data
        }

# Placeholder for report data. Reports might be too diverse for a single ORM model.
# Direct SQL queries and potentially materialized views are often better for complex reports.
class ReportData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.String, nullable=False, index=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    # ... other columns for report data ...

    # No serialize method here as report data is typically fetched via direct queries
    # and shaped as needed.

# Example of how to define other models and indexes
# db.Index('idx_user_report', ReportData.user_id, ReportData.report_id)
