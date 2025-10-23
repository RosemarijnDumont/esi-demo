import time

class ThrottlingMechanism:
    def __init__(self, time_window_seconds=3600, max_emails_per_window=3):
        self.customer_activity = {}
        self.time_window_seconds = time_window_seconds
        self.max_emails_per_window = max_emails_per_window

    def can_send_email(self, customer_id, inquiry_type):
        current_time = time.time()

        if customer_id not in self.customer_activity:
            self.customer_activity[customer_id] = []

        # Remove old entries outside the time window
        self.customer_activity[customer_id] = [
            (ts, it) for (ts, it) in self.customer_activity[customer_id]
            if current_time - ts < self.time_window_seconds
        ]

        # Count emails of the same type within the window
        same_type_emails_in_window = [
            (ts, it) for (ts, it) in self.customer_activity[customer_id]
            if it == inquiry_type
        ]

        if len(same_type_emails_in_window) < self.max_emails_per_window:
            self.customer_activity[customer_id].append((current_time, inquiry_type))
            return True
        else:
            print(f"Throttling: Customer {customer_id} has exceeded the email limit for inquiry type '{inquiry_type}'.")
            return False
