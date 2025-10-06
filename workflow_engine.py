import datetime
import logging
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WorkflowEngine:
    def __init__(self):
        self.schedules: Dict[str, Dict] = {}
        self.hcat_system = HCATSystem() # Assuming an HCATSystem exists and can be integrated

    def define_schedule(self, schedule_name: str, schedule_config: Dict):
        """
        Defines or updates a cleaning schedule.

        Args:
            schedule_name: A unique name for the schedule (e.g., "daily_morning", "weekly_evening").
            schedule_config: A dictionary containing schedule details:
                             - 'team_id': ID of the team responsible.
                             - 'frequency_type': "daily", "weekly", "ad-hoc".
                             - 'start_time': (For daily/weekly) Time in HH:MM format.
                             - 'day_of_week': (For weekly) List of integers (0=Monday, 6=Sunday).
        """
        self.schedules[schedule_name] = schedule_config
        logging.info(f"Schedule '{schedule_name}' defined/updated: {schedule_config}")

    def get_responsible_team(self, schedule_name: str, context_date: Optional[datetime.date] = None) -> Optional[str]:
        """
        Identifies the responsible team for a given schedule and date.

        Args:
            schedule_name: The name of the schedule.
            context_date: The date for which to check the schedule. Defaults to today.

        Returns:
            The team ID if a team is responsible, otherwise None.
        """
        schedule = self.schedules.get(schedule_name)
        if not schedule:
            logging.warning(f"Schedule '{schedule_name}' not found.")
            return None

        team_id = schedule.get('team_id')
        if not team_id:
            logging.warning(f"Team ID not configured for schedule '{schedule_name}'.")
            return None

        frequency_type = schedule.get('frequency_type')
        if not frequency_type:
            logging.warning(f"Frequency type not configured for schedule '{schedule_name}'.")
            return None

        if frequency_type == "ad-hoc":
            return team_id  # Ad-hoc always returns the assigned team

        if context_date is None:
            context_date = datetime.date.today()

        if frequency_type == "daily":
            return team_id
        elif frequency_type == "weekly":
            day_of_week = schedule.get('day_of_week', [])
            if context_date.weekday() in day_of_week:
                return team_id
        else:
            logging.warning(f"Unknown frequency type '{frequency_type}' for schedule '{schedule_name}'.")

        return None

    def trigger_task(self, schedule_name: str, adhoc_reason: Optional[str] = None) -> bool:
        """
        Triggers a cleaning task based on the schedule or an ad-hoc request.

        Args:
            schedule_name: The name of the schedule to trigger.
            adhoc_reason: Optional reason for an ad-hoc request.

        Returns:
            True if the HCAT was successfully generated and dispatched, False otherwise.
        """
        team_id = self.get_responsible_team(schedule_name)
        if team_id:
            task_description = f"Kitchen cleaning required for schedule '{schedule_name}'."
            if adhoc_reason:
                task_description += f" Reason: {adhoc_reason}"

            hcat_success = self.hcat_system.generate_and_dispatch_hcat(team_id, task_description)
            if hcat_success:
                logging.info(f"HCAT successfully dispatched to team '{team_id}' for schedule '{schedule_name}'.")
                return True
            else:
                logging.error(f"Failed to dispatch HCAT for team '{team_id}' and schedule '{schedule_name}'.")
                return False
        else:
            logging.info(f"No responsible team found for schedule '{schedule_name}' for today. Skipping HCAT generation.")
            return False

class HCATSystem:
    """
    A mock HCAT (Housekeeping Check-in/Check-out) system for integration.
    In a real system, this would interact with an external API or messaging service.
    """
    def generate_and_dispatch_hcat(self, team_id: str, description: str) -> bool:
        """
        Generates and dispatches an HCAT.

        Args:
            team_id: The ID of the team to send the HCAT to.
            description: The description of the task.

        Returns:
            True if HCAT is assumed to be dispatched, False otherwise (for simulation purposes).
        """
        logging.info(f"[HCAT SYSTEM] Generating HCAT for Team: {team_id}, Task: {description}")
        # Simulate HCAT delivery confirmation
        return True


class Scheduler:
    def __init__(self, workflow_engine: WorkflowEngine):
        self.workflow_engine = workflow_engine
    
    def run_scheduled_tasks(self):
        """
        Checks all defined schedules and triggers tasks if they are due.
        This method would typically be called by a cron job or a background process.
        """
        logging.info("Running scheduled tasks...")
        for schedule_name, schedule_config in self.workflow_engine.schedules.items():
            if schedule_config.get('frequency_type') != 'ad-hoc':
                # For daily/weekly schedules, check if today is a relevant day
                team = self.workflow_engine.get_responsible_team(schedule_name, datetime.date.today())
                if team:
                    # Further check if the current time is around 'start_time' if desired
                    # For simplicity, we'll just trigger if the day matches.
                    logging.info(f"Scheduled task '{schedule_name}' due today. Triggering.")
                    self.workflow_engine.trigger_task(schedule_name)
                else:
                    logging.info(f"Scheduled task '{schedule_name}' not due today.")
        logging.info("Finished running scheduled tasks.")


# API endpoint simulation (e.g., using Flask/FastAPI)
from flask import Flask, request, jsonify

app = Flask(__name__)
engine = WorkflowEngine()
scheduler_instance = Scheduler(engine)

# Example schedule configurations
engine.define_schedule(
    "daily_kitchen_morning",
    {"team_id": "TeamA", "frequency_type": "daily", "start_time": "08:00"}
)
engine.define_schedule(
    "weekly_kitchen_evening",
    {"team_id": "TeamB", "frequency_type": "weekly", "start_time": "19:00", "day_of_week": [2, 4]}  # Wednesday, Friday
)
engine.define_schedule(
    "ad_hoc_urgent_cleaning",
    {"team_id": "TeamC", "frequency_type": "ad-hoc"}
)

@app.route('/trigger_ad_hoc_cleaning', methods=['POST'])
def trigger_ad_hoc_cleaning():
    data = request.get_json()
    schedule_name = data.get('schedule_name')
    reason = data.get('reason')

    if not schedule_name:
        return jsonify({"status": "error", "message": "'schedule_name' is required."}), 400

    schedule_config = engine.schedules.get(schedule_name)
    if not schedule_config or schedule_config.get('frequency_type') != 'ad-hoc':
        return jsonify({"status": "error", "message": f"Schedule '{schedule_name}' not found or is not an ad-hoc schedule."}), 404

    if engine.trigger_task(schedule_name, adhoc_reason=reason):
        return jsonify({"status": "success", "message": f"Ad-hoc cleaning request for '{schedule_name}' triggered."}), 200
    else:
        return jsonify({"status": "failure", "message": f"Failed to trigger ad-hoc cleaning request for '{schedule_name}'."}), 500

@app.route('/define_cleaning_schedule', methods=['POST'])
def define_cleaning_schedule():
    data = request.get_json()
    schedule_name = data.get('schedule_name')
    schedule_config = data.get('schedule_config')

    if not schedule_name or not schedule_config:
        return jsonify({"status": "error", "message": "'schedule_name' and 'schedule_config' are required."}), 400
    
    # Basic validation for schedule_config
    required_keys = ['team_id', 'frequency_type']
    if not all(key in schedule_config for key in required_keys):
        return jsonify({"status": "error", "message": f"schedule_config must contain: {', '.join(required_keys)}"}), 400

    engine.define_schedule(schedule_name, schedule_config)
    return jsonify({"status": "success", "message": f"Schedule '{schedule_name}' defined successfully."}), 200

@app.route('/run_daily_schedule', methods=['GET'])
def run_daily_schedule():
    """
    This endpoint simulates a daily trigger for scheduled tasks.
    In production, this would be a CRON job or similar.
    """
    scheduler_instance.run_scheduled_tasks()
    return jsonify({"status": "success", "message": "Daily schedule run initiated."}), 200


if __name__ == '__main__':
    # To run the API:
    # flask run
    # Or directly for development:
    # app.run(debug=True)
    # For scheduled tasks, you'd typically have a separate process or cron job
    # calling `scheduler_instance.run_scheduled_tasks()` at the appropriate times.
    print("To start the Flask API, run 'flask run' in your terminal.")
    print("Example usage:")
    print("  POST /define_cleaning_schedule with {'schedule_name': 'new_schedule', 'schedule_config': {'team_id': 'TeamX', 'frequency_type': 'daily'}}")
    print("  POST /trigger_ad_hoc_cleaning with {'schedule_name': 'ad_hoc_urgent_cleaning', 'reason': 'Spill in kitchen'}")
    print("  GET /run_daily_schedule (simulates daily cron job)")


