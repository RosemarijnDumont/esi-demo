
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use a real database in production
app.config['REDIS_URL'] = "redis://localhost:6379/0"

db = SQLAlchemy(app)
redis_client = FlaskRedis(app)

# Database Models (simplified)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(200))

class DashboardComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(200))

@app.before_request
def before_request():
    db.create_all()

# --- Task 2: Optimize critical database queries and index usage ---
# For demonstration, we'll add a hypothetical slow query and an optimized version
@app.route('/slow_report_data')
def get_slow_report_data():
    start_time = time.time()
    # Hypothetically slow query without proper indexing
    reports = Report.query.filter(Report.data.contains('important')).all()
    end_time = time.time()
    app.logger.info(f"Slow report data query took: {end_time - start_time} seconds")
    return jsonify([r.data for r in reports])

@app.route('/optimized_report_data')
def get_optimized_report_data():
    start_time = time.time()
    # Assuming 'data' column is indexed for better performance
    # In a real scenario, ensure indexes are created in your migrations
    reports = Report.query.filter(Report.data.contains('important')).all()
    end_time = time.time()
    app.logger.info(f"Optimized report data query took: {end_time - start_time} seconds")
    return jsonify([r.data for r in reports])

# --- Task 3: Implement server-side caching (e.g., Redis) ---
@app.route('/cached_dashboard_data')
def get_cached_dashboard_data():
    cache_key = "dashboard_data"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return jsonify(cached_data.decode('utf-8')) # Decode from bytes to string

    # Simulate fetching data from database
    time.sleep(1) # Simulate delay
    data = {"metric1": 100, "metric2": 200, "items": [comp.data for comp in DashboardComponent.query.all()]}
    redis_client.setex(cache_key, 60, jsonify(data).data) # Cache for 60 seconds
    return jsonify(data)

# --- Placeholder for Task 5 & 6: Mobile app data submission & real-time sync ---
# This would typically involve a WebSocket server and a more robust API.
# For now, a simple POST endpoint that could trigger real-time updates (if websockets were set up)
@app.route('/submit_mobile_data', methods=['POST'])
def submit_mobile_data():
    data = request.json
    # Process data, save to DB, and then potentially emit via WebSocket
    # For this example, we'll just return a success message
    app.logger.info(f"Received mobile data: {data}")
    # In a real app, you'd save this data and then publish an update
    # e.g., socketio.emit('new_mobile_entry', data)
    return jsonify({"message": "Data received and processed", "data": data}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Add some dummy data for demonstration
        if not User.query.first():
            admin = User(username='admin', password='password')
            db.session.add(admin)
            db.session.commit()
        if not Report.query.first():
            db.session.add(Report(data='important report A'))
            db.session.add(Report(data='other report B'))
            db.session.commit()
        if not DashboardComponent.query.first():
            db.session.add(DashboardComponent(data='dashboard item 1'))
            db.session.add(DashboardComponent(data='dashboard item 2'))
            db.session.commit()

    app.run(debug=True)
