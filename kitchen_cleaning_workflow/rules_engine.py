
import datetime

class KitchenCleaningRulesEngine:
    def __init__(self, schedule_config):
        self.schedule_config = schedule_config

    def get_responsible_team(self, current_datetime):
        # Implement logic to interpret schedule_config and determine the responsible team
        # Example: schedule_config could be a list of dictionaries with 'day_of_week', 'time_range', 'team'
        # For simplicity, let's assume a rotating team weekly based on the schedule_config
        # schedule_config = {
        #    "weekly_rotation": {
        #        0: "Team A", # Monday
        #        1: "Team B", # Tuesday
        #        2: "Team C", # Wednesday
        #        3: "Team D", # Thursday
        #        4: "Team E", # Friday
        #        5: "Team F", # Saturday
        #        6: "Team G"  # Sunday
        #    }
        # }
        
        day_of_week = current_datetime.weekday()
        if "weekly_rotation" in self.schedule_config:
            return self.schedule_config["weekly_rotation"].get(day_of_week)
        
        return "Default Team" # Fallback

    def is_cleaning_required(self, current_datetime):
        # Implement logic to check if cleaning is required based on schedule and thresholds
        # For now, let's assume cleaning is required daily at a certain time
        
        cleaning_time = self.schedule_config.get("cleaning_time", "17:00")
        cleaning_hour, cleaning_minute = map(int, cleaning_time.split(":"))

        return current_datetime.hour == cleaning_hour and current_datetime.minute == cleaning_minute

