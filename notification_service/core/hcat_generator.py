import uuid
from datetime import datetime

class HCATGenerator:
    @staticmethod
    def generate_hcat_message(task_id: str, task_type: str, location: str, team_id: str, due_time: str = None, priority: str = "medium") -> str:
        """
        Generates a structured HCAT (Housekeeping Check-in/Check-out) message.

        Args:
            task_id (str): Unique identifier for the cleaning task.
            task_type (str): Type of cleaning task (e.g., 'kitchen cleaning', 'restroom cleaning').
            location (str): Specific location for the cleaning task (e.g., 'Main Kitchen', 'Floor 3 Breakroom').
            team_id (str): Identifier of the team assigned to the task (e.g., 'kitchen_crew_a').
            due_time (str, optional): The time the task is due, in a human-readable format. Defaults to None.
            priority (str, optional): The priority of the task (e.g., 'low', 'medium', 'high', 'urgent'). Defaults to 'medium'.

        Returns:
            str: A formatted HCAT message string.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"""
HCAT Notification - {task_type.replace('_', ' ').title()}
------------------------------------------------
Task ID: {task_id}
Type: {task_type.replace('_', ' ').title()}
Location: {location}
Assigned Team: {team_id}
Priority: {priority.upper()}
Generated At: {current_time}
"""
        if due_time:
            message += f"Due By: {due_time}\n"
        message += "\nPlease address this task promptly."
        return message

    @staticmethod
    def generate_task_id(prefix: str = "HCAT") -> str:
        """
        Generates a unique task ID.
        """
        return f"{prefix}-{uuid.uuid4()}"
