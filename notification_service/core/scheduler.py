from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import logging
import atexit
import requests
import json
from notification_service.data.data_store import DataStore
from notification_service.core.hcat_generator import HCATGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Scheduler:
    scheduler = BackgroundScheduler()
    NOTIFICATION_SERVICE_BASE_URL = "http://127.0.0.1:5001" # Assuming local Flask service

    @classmethod
    def start(cls):
        if not cls.scheduler.running:
            cls.scheduler.start()
            logging.info("Scheduler started.")
            atexit.register(lambda: cls.scheduler.shutdown())
            cls.load_and_schedule_tasks()
        else:
            logging.info("Scheduler is already running.")

    @classmethod
    def load_and_schedule_tasks(cls):
        cls.scheduler.remove_all_jobs()
        logging.info("Removed all existing jobs from the scheduler.")
        schedule_entries = DataStore.get_cleaning_schedule()
        logging.info("Loading %d schedule entries.", len(schedule_entries))

        for entry in schedule_entries:
            cls.add_scheduled_task(entry)
        logging.info("All tasks from DataStore have been scheduled.")

    @classmethod
    def add_scheduled_task(cls, entry: dict):
        day_of_week_map = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
        }
        day_of_week = day_of_week_map.get(entry['day_of_week'].lower())
        if day_of_week is None:
            logging.warning("Invalid day_of_week in schedule entry: %s. Skipping.", entry)
            return

        try:
            hour, minute = map(int, entry['time'].split(':'))
        except ValueError:
            logging.error("Invalid time format in schedule entry: %s. Expected HH:MM. Skipping.", entry)
            return

        task_id = HCATGenerator.generate_task_id(f"{entry['task_type'].replace(' ', '_').upper()}")
        team_config = DataStore.get_team_config(entry['team_id'])
        if not team_config:
            logging.error("Team configuration not found for team_id: %s. Cannot schedule task %s.", entry['team_id'], task_id)
            return

        # Dynamically calculate the next due_time based on scheduling
        now = datetime.now()
        next_run_date = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Adjust for the correct day of the week if it's in the past this week
        current_day_of_week = now.weekday() # Monday is 0 and Sunday is 6
        if current_day_of_week > day_of_week or (current_day_of_week == day_of_week and now > next_run_date):
            # If the scheduled day has passed this week or it's today but the time has passed, schedule for next week
            days_to_add = (7 - current_day_of_week + day_of_week) % 7
            if days_to_add == 0: # If it's the same day but passed, add 7 days
                days_to_add = 7
            next_run_date += timedelta(days=days_to_add)
        else:
            # If the scheduled day is later this week or today and the time is in the future
            days_to_add = day_of_week - current_day_of_week
            next_run_date += timedelta(days=days_to_add)



        due_time_str = next_run_date.strftime("%Y-%m-%d %H:%M:%S")

        trigger_data = {
            "task_id": task_id,
            "task_type": entry['task_type'],
            "location": entry['location'],
            "team_id": entry['team_id'],
            "due_time": due_time_str,
            "priority": entry.get('priority', 'medium')
        }

        job_id = f"hcat_task_{task_id}"
        cls.scheduler.add_job(
            cls._trigger_hcat_webhook,
            trigger='cron',
            day_of_week=day_of_week,
            hour=hour,
            minute=minute,
            args=[trigger_data],
            id=job_id,
        )
        logging.info("Scheduled HCAT task '%s' for team '%s' at %s %s:%s. Trigger data: %s",
                     job_id, entry['team_id'], entry['day_of_week'], hour, minute, trigger_data)

    @classmethod
    def _trigger_hcat_webhook(cls, trigger_data: dict):
        logging.info("Attempting to trigger HCAT webhook for task_id: %s", trigger_data['task_id'])
        try:
            response = requests.post(f"{cls.NOTIFICATION_SERVICE_BASE_URL}/trigger_hcat", json=trigger_data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            logging.info("HCAT trigger for task_id %s successful: %s", trigger_data['task_id'], response.json())
        except requests.exceptions.RequestException as e:
            logging.error("Error triggering HCAT webhook for task_id %s: %s", trigger_data['task_id'], e)

# Ensure the scheduler starts when this module is imported, but only once.
# It's better to explicitly call Scheduler.start() from the main app or a dedicated entrypoint.
# However, for a simple Flask app running directly, this can ensure scheduling is activated.
# Consider externalizing this for production or using a separate worker process.
# Scheduler.start()


