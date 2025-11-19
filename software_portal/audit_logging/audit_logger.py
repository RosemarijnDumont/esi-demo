import json
from datetime import datetime

class AuditLogger:
    """
    Provides audit logging functionality for all actions and approvals.
    """
    def __init__(self, log_file="audit.log"):
        self.log_file = log_file

    def log(self, event_type, user_id, entity_id, details=None):
        """
        Logs an audit event.
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "entity_id": entity_id, # e.g., request_id, license_id, deployment_id
            "details": details if details is not None else {}
        }

        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
            print(f"Audit logged: {event_type} by {user_id} for {entity_id}")
        except IOError as e:
            print(f"Error writing to audit log file: {e}")

    def get_logs(self, limit=100):
        """
        Reads the latest audit logs from the file.
        """
        logs = []
        try:
            with open(self.log_file, "r") as f:
                for line in f:
                    logs.append(json.loads(line))
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from audit log: {e}")
            return []
        return logs[-limit:] # Return latest logs