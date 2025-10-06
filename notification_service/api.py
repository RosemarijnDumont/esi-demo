from flask import Blueprint, request, jsonify
import logging
from notification_service.core.hcat_generator import HCATGenerator
from notification_service.core.notification_sender import NotificationSender
from notification_service.data.data_store import DataStore
from notification_service.utils.notifier_factory import NotifierFactory

notification_bp = Blueprint('notification', __name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@notification_bp.route('/trigger_hcat', methods=['POST'])
def trigger_hcat():
    data = request.json
    if not data or not all(k in data for k in ['task_id', 'task_type', 'location', 'team_id']):
        logging.error("Invalid payload for trigger_hcat: %s", data)
        return jsonify({"error": "Missing required fields (task_id, task_type, location, team_id)"}), 400

    task_id = data['task_id']
    task_type = data['task_type']
    location = data['location']
    team_id = data['team_id']
    due_time = data.get('due_time')
    priority = data.get('priority', 'medium')

    logging.info("Received HCAT trigger for task_id: %s, team_id: %s", task_id, team_id)

    # Generate HCAT message
    hcat_message = HCATGenerator.generate_hcat_message(
        task_id=task_id,
        task_type=task_type,
        location=location,
        team_id=team_id,
        due_time=due_time,
        priority=priority
    )

    # Get notifier based on team_id (or configure a default)
    team_config = DataStore.get_team_config(team_id)
    if not team_config:
        logging.error("Team configuration not found for team_id: %s", team_id)
        return jsonify({"error": f"Team configuration not found for team_id {team_id}"}), 404

    notification_channel = team_config.get('notification_channel', 'email') # Default to email
    recipient = team_config.get('recipient')

    if not recipient:
        logging.error("Recipient not configured for team_id: %s in channel: %s", team_id, notification_channel)
        return jsonify({"error": f"Recipient not configured for team {team_id} in {notification_channel}"}), 500

    notifier = NotifierFactory.get_notifier(notification_channel)
    if not notifier:
        logging.error("Notifier not found for channel: %s", notification_channel)
        return jsonify({"error": f"Notifier not found for channel {notification_channel}"}), 500

    sender = NotificationSender(notifier)
    success = sender.send_notification(
        recipient=recipient,
        subject=f"HCAT: {task_type} at {location}",
        message=hcat_message,
        task_id=task_id
    )

    if success:
        logging.info("HCAT successfully triggered and sent for task_id: %s to team_id: %s", task_id, team_id)
        return jsonify({"message": "HCAT triggered and sent successfully", "task_id": task_id}), 200
    else:
        logging.error("Failed to send HCAT for task_id: %s to team_id: %s", task_id, team_id)
        return jsonify({"error": "Failed to trigger and send HCAT"}), 500