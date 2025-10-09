
class HCATGenerator:
    def __init__(self, notification_service):
        self.notification_service = notification_service # This would be an external service to send notifications

    def generate_hcat(self, team, cleaning_details):
        hcat_message = f"HCAT: Kitchen cleaning required for {team}. Details: {cleaning_details}"
        print(f"Generated HCAT: {hcat_message}")
        # In a real system, self.notification_service.send_notification(team, hcat_message)
        return hcat_message

    def log_hcat_delivery(self, hcat_message, team, status="Sent"):
        print(f"HCAT '{hcat_message}' delivered to {team} with status: {status}")
        # In a real system, log this to a database or a logging service

