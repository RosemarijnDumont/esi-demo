
from flask import Flask, request, jsonify
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# In-memory store for demonstration purposes
# In a real application, this would be a database
cleaning_schedule = {
    "monday": "Team A",
    "tuesday": "Team B",
    "wednesday": "Team C",
    "thursday": "Team A",
    "friday": "Team B",
    "saturday": "Team C",
    "sunday": "Team A",
}

hcat_logs = []

def generate_hcat_content(team_name, date):
    """Generates the HCAT content based on team and date."""
    return f"HCAT: Kitchen Cleaning Assignment for {team_name} on {date}. Please ensure all kitchen areas are thoroughly cleaned."

def send_notification(team_name, hcat_content):
    """Simulates sending a notification to the specified team."
    """Simulates sending a notification to the specified team.
    In a production environment, this would integrate with an actual messaging platform (e.g., email, Slack, Teams).
    """
    try:
        logging.info(f"Sending HCAT to {team_name}: {hcat_content}")
        # Simulate a successful delivery
        return {"status": "sent", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        logging.error(f"Failed to send HCAT to {team_name}: {e}")
        return {"status": "failed", "error": str(e), "timestamp": datetime.now().isoformat()}

def log_hcat_delivery(team, hcat_content, delivery_status):
    """Logs the HCAT delivery confirmation."""
    log_entry = {
        "team": team,
        "hcat_content": hcat_content,
        "delivery_status": delivery_status["status"],
        "timestamp": delivery_status["timestamp"],
        "delivery_details": delivery_status
    }
    hcat_logs.append(log_entry)
    logging.info(f"HCAT delivery logged: {log_entry}")

@app.route('/hcat/generate-and-send', methods=['POST'])
def generate_and_send_hcat():
    """
    API endpoint for the Workflow Engine to request HCAT generation and sending.
    Expected JSON payload: 
    {
        "date": "YYYY-MM-DD" (optional, defaults to today),
        "team": "Team Name" (optional, overrides schedule)
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    target_date_str = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    try:
        target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    day_of_week = target_date.strftime('%A').lower()
    
    team_name = data.get('team')
    if not team_name:
        team_name = cleaning_schedule.get(day_of_week)
        if not team_name:
            return jsonify({"error": f"No team assigned for {day_of_week} in the schedule."}), 404

    hcat_content = generate_hcat_content(team_name, target_date_str)
    delivery_status = send_notification(team_name, hcat_content)
    log_hcat_delivery(team_name, hcat_content, delivery_status)

    if delivery_status["status"] == "sent":
        return jsonify({
            "message": "HCAT generated and sent successfully",
            "team": team_name,
            "date": target_date_str,
            "hcat_content": hcat_content,
            "delivery_status": delivery_status
        }), 200
    else:
        return jsonify({
            "message": "Failed to send HCAT",
            "team": team_name,
            "date": target_date_str,
            "hcat_content": hcat_content,
            "delivery_status": delivery_status,
            "error": delivery_status.get("error")
        }), 500

@app.route('/schedule', methods=['GET'])
def get_schedule():
    """Returns the current cleaning schedule."""
    return jsonify(cleaning_schedule), 200

@app.route('/schedule', methods=['POST'])
def update_schedule():
    """Updates the cleaning schedule.
    Expected JSON payload: {"day_of_week": "Team Name", ...}
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    
    for day, team in data.items():
        if day.lower() in cleaning_schedule:
            cleaning_schedule[day.lower()] = team
        else:
            return jsonify({"error": f"Invalid day of week: {day}. Must be one of Monday-Sunday."}), 400
            
    return jsonify({"message": "Schedule updated successfully", "new_schedule": cleaning_schedule}), 200

@app.route('/hcat/logs', methods=['GET'])
def get_hcat_logs():
    """Returns all logged HCAT delivery confirmations."""
    return jsonify(hcat_logs), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
