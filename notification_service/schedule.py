from flask import Blueprint, request, jsonify
import logging
from notification_service.data.data_store import DataStore
from notification_service.core.scheduler import Scheduler

schedule_bp = Blueprint('schedule', __name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@schedule_bp.route('/cleaning_schedule', methods=['GET'])
def get_cleaning_schedule():
    schedule = DataStore.get_cleaning_schedule()
    return jsonify(schedule), 200

@schedule_bp.route('/cleaning_schedule', methods=['POST'])
def add_cleaning_schedule_entry():
    data = request.json
    if not data or not all(k in data for k in ['day_of_week', 'time', 'team_id', 'location', 'task_type']):
        logging.error("Invalid payload for add_cleaning_schedule_entry: %s", data)
        return jsonify({"error": "Missing required fields (day_of_week, time, team_id, location, task_type)"}), 400

    DataStore.add_cleaning_schedule_entry(data)
    Scheduler.load_and_schedule_tasks()
    logging.info("Added new cleaning schedule entry: %s", data)
    return jsonify({"message": "Cleaning schedule entry added successfully"}), 201

@schedule_bp.route('/cleaning_schedule/<string:schedule_id>', methods=['PUT'])
def update_cleaning_schedule_entry(schedule_id):
    data = request.json
    if not data:
        logging.error("Invalid payload for update_cleaning_schedule_entry: No data provided")
        return jsonify({"error": "No data provided for update"}), 400

    success = DataStore.update_cleaning_schedule_entry(schedule_id, data)
    if success:
        Scheduler.load_and_schedule_tasks()
        logging.info("Updated cleaning schedule entry ID %s with data: %s", schedule_id, data)
        return jsonify({"message": f"Cleaning schedule entry {schedule_id} updated successfully"}), 200
    else:
        logging.warning("Cleaning schedule entry ID %s not found for update", schedule_id)
        return jsonify({"error": f"Cleaning schedule entry {schedule_id} not found"}), 404

@schedule_bp.route('/cleaning_schedule/<string:schedule_id>', methods=['DELETE'])
def delete_cleaning_schedule_entry(schedule_id):
    success = DataStore.delete_cleaning_schedule_entry(schedule_id)
    if success:
        Scheduler.load_and_schedule_tasks()
        logging.info("Deleted cleaning schedule entry ID: %s", schedule_id)
        return jsonify({"message": f"Cleaning schedule entry {schedule_id} deleted successfully"}), 200
    else:
        logging.warning("Cleaning schedule entry ID %s not found for deletion", schedule_id)
        return jsonify({"error": f"Cleaning schedule entry {schedule_id} not found"}), 404

@schedule_bp.route('/teams', methods=['GET'])
def get_teams():
    teams = DataStore.get_all_team_configs()
    return jsonify(teams), 200

@schedule_bp.route('/teams', methods=['POST'])
def add_team_config():
    data = request.json
    if not data or not all(k in data for k in ['team_id', 'team_name', 'notification_channel', 'recipient']):
        logging.error("Invalid payload for add_team_config: %s", data)
        return jsonify({"error": "Missing required fields (team_id, team_name, notification_channel, recipient)"}), 400

    DataStore.add_team_config(data)
    logging.info("Added new team configuration: %s", data['team_id'])
    return jsonify({"message": "Team configuration added successfully"}), 201

@schedule_bp.route('/teams/<string:team_id>', methods=['PUT'])
def update_team_config(team_id):
    data = request.json
    if not data:
        logging.error("Invalid payload for update_team_config: No data provided")
        return jsonify({"error": "No data provided for update"}), 400

    success = DataStore.update_team_config(team_id, data)
    if success:
        logging.info("Updated team configuration for team_id %s with data: %s", team_id, data)
        return jsonify({"message": f"Team configuration for {team_id} updated successfully"}), 200
    else:
        logging.warning("Team configuration for team_id %s not found for update", team_id)
        return jsonify({"error": f"Team configuration for {team_id} not found"}), 404

@schedule_bp.route('/teams/<string:team_id>', methods=['DELETE'])
def delete_team_config(team_id):
    success = DataStore.delete_team_config(team_id)
    if success:
        logging.info("Deleted team configuration for team_id: %s", team_id)
        return jsonify({"message": f"Team configuration for {team_id} deleted successfully"}), 200
    else:
        logging.warning("Team configuration for team_id %s not found for deletion", team_id)
        return jsonify({"error": f"Team configuration for {team_id} not found"}), 404
