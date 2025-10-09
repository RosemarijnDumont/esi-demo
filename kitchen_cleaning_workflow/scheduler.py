
import datetime
import time

class KitchenCleaningScheduler:
    def __init__(self, rules_engine, hcat_generator, interval_seconds=60):
        self.rules_engine = rules_engine
        self.hcat_generator = hcat_generator
        self.interval_seconds = interval_seconds
        self._running = False

    def start(self):
        self._running = True
        print("Kitchen Cleaning Scheduler started.")
        while self._running:
            self._check_and_trigger()
            time.sleep(self.interval_seconds)

    def stop(self):
        self._running = False
        print("Kitchen Cleaning Scheduler stopped.")

    def _check_and_trigger(self):
        current_datetime = datetime.datetime.now()
        if self.rules_engine.is_cleaning_required(current_datetime):
            team = self.rules_engine.get_responsible_team(current_datetime)
            if team:
                cleaning_details = "Routine daily kitchen cleaning"
                hcat_message = self.hcat_generator.generate_hcat(team, cleaning_details)
                self.hcat_generator.log_hcat_delivery(hcat_message, team)
            else:
                print("No responsible team found for today's cleaning.")

    def trigger_ad_hoc_cleaning(self, team, cleaning_details="Ad-hoc kitchen cleaning request"):
        print(f"Ad-hoc cleaning request triggered for {team}: {cleaning_details}")
        hcat_message = self.hcat_generator.generate_hcat(team, cleaning_details)
        self.hcat_generator.log_hcat_delivery(hcat_message, team)

