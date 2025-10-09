
from kitchen_cleaning_workflow.rules_engine import KitchenCleaningRulesEngine
from kitchen_cleaning_workflow.hcat_generator import HCATGenerator
from kitchen_cleaning_workflow.scheduler import KitchenCleaningScheduler
from kitchen_cleaning_workflow.workflow_state import WorkflowStateManager
import threading
import time

# --- Configuration ---
# This schedule_config can be loaded from a database or a configuration file in a real application
schedule_config = {
    "weekly_rotation": {
        0: "Team Alpha", # Monday
        1: "Team Beta",  # Tuesday
        2: "Team Gamma", # Wednesday
        3: "Team Delta", # Thursday
        4: "Team Epsilon", # Friday
        5: "Team Zeta",  # Saturday
        6: "Team Eta"    # Sunday
    },
    "cleaning_time": "17:00" # HH:MM format
}

class MockNotificationService:
    def send_notification(self, team, message):
        print(f"Mock Notification Service: Sending '{message}' to {team}")

if __name__ == "__main__":
    # Initialize components
    rules_engine = KitchenCleaningRulesEngine(schedule_config)
    notification_service = MockNotificationService() # In a real app, this would be a concrete notification service
    hcat_generator = HCATGenerator(notification_service)
    workflow_state_manager = WorkflowStateManager()

    # Override HCATGenerator's log_hcat_delivery to interact with WorkflowStateManager
    original_log_hcat_delivery = hcat_generator.log_hcat_delivery
    def custom_log_hcat_delivery(hcat_message, team, status="Sent"):
        original_log_hcat_delivery(hcat_message, team, status)
        workflow_state_manager.add_assignment(team, hcat_message, status)
    hcat_generator.log_hcat_delivery = custom_log_hcat_delivery

    scheduler = KitchenCleaningScheduler(rules_engine, hcat_generator, interval_seconds=10) # Check every 10 seconds for demo

    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=scheduler.start)
    scheduler_thread.daemon = True  # Allow the main program to exit even if the thread is running
    scheduler_thread.start()

    print("Workflow Engine started. Waiting for scheduled cleaning tasks or ad-hoc requests...")
    print("You can trigger ad-hoc requests by calling scheduler.trigger_ad_hoc_cleaning(team, details).")
    print("Example: scheduler.trigger_ad_hoc_cleaning('AdHoc Team', 'Urgent spill cleanup')")
    print("To view workflow state: workflow_state_manager.get_all_assignments()")

    try:
        while True:
            # This loop keeps the main thread alive, allowing the scheduler thread to run
            # and also allows for manual interaction (e.g., ad-hoc triggers from a console)
            time.sleep(1)
            # Example ad-hoc trigger (can be uncommented for testing)
            # if datetime.datetime.now().second == 0 and datetime.datetime.now().minute % 2 == 0:
            #     scheduler.trigger_ad_hoc_cleaning("Emergency Team", "Overflowing sink")
            #     time.sleep(2) # Avoid multiple triggers in a single second

    except KeyboardInterrupt:
        print("Stopping workflow engine...")
        scheduler.stop()
        scheduler_thread.join() # Wait for the scheduler thread to finish (optional)
        print("Workflow engine stopped.")

