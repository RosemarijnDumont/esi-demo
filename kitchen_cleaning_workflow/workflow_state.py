
import json
import os
import datetime

class WorkflowStateManager:
    def __init__(self, state_file="workflow_state.json"):
        self.state_file = state_file
        self.workflow_state = self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                return json.load(f)
        return {"assignments": []}

    def _save_state(self):
        with open(self.state_file, "w") as f:
            json.dump(self.workflow_state, f, indent=4)

    def add_assignment(self, team, hcat_message, status="Pending"):
        assignment = {
            "timestamp": datetime.datetime.now().isoformat(),
            "team": team,
            "hcat_message": hcat_message,
            "status": status
        }
        self.workflow_state["assignments"].append(assignment)
        self._save_state()
        print(f"Assignment added: {assignment}")

    def update_assignment_status(self, hcat_message, new_status):
        for assignment in self.workflow_state["assignments"]:
            if assignment["hcat_message"] == hcat_message:
                assignment["status"] = new_status
                self._save_state()
                print(f"Assignment '{hcat_message}' status updated to '{new_status}'")
                return
        print(f"Assignment with HCAT message '{hcat_message}' not found.")

    def get_all_assignments(self):
        return self.workflow_state["assignments"]

    def get_assignments_by_status(self, status):
        return [a for a in self.workflow_state["assignments"] if a["status"] == status]

