from flask import Flask, request, jsonify
from notification_service.api import notification_bp
from notification_service.schedule import schedule_bp

app = Flask(__name__)
app.register_blueprint(notification_bp)
app.register_blueprint(schedule_bp)

@app.route('/')
def health_check():
    return jsonify({"status": "Notification Service Up"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)