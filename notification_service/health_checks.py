import logging
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NotificationHealthChecker:
    """
    A class to manage health checks and monitoring for notification queues and workers.
    """
    def __init__(self, queue_names, worker_names, max_queue_backlog=100, max_worker_downtime_seconds=300):
        self.queue_names = queue_names
        self.worker_names = worker_names
        self.max_queue_backlog = max_queue_backlog
        self.max_worker_downtime_seconds = max_worker_downtime_seconds
        self.worker_last_seen = {worker: datetime.datetime.now() for worker in worker_names}

    def _get_queue_status(self, queue_name):
        """
        Simulates getting the status of a notification queue.
        In a real scenario, this would interact with a message queue service (e.g., RabbitMQ, Kafka, SQS).
        Returns a tuple: (current_backlog_size, is_healthy).
        """\n        # Placeholder for actual queue monitoring logic
        # For demonstration, we'll simulate some backlogs.
        if "critical" in queue_name:
            return 50, True # Critical queue usually healthy
        elif "marketing" in queue_name:
            return 150, False # Marketing queue might have more backlog
        else:
            return 10, True

    def _get_worker_status(self, worker_name):
        """
        Simulates getting the status of a notification worker.
        In a real scenario, this would check worker process status, heartbeat, etc.
        Returns a tuple: (is_running, last_heartbeat_timestamp).
        """
        # Placeholder for actual worker monitoring logic
        # For demonstration, we'll simulate worker status.
        if "email-worker-1" == worker_name:
            # Simulate a worker that might go down sometimes
            if (datetime.datetime.now() - self.worker_last_seen[worker_name]).total_seconds() > 600:
                self.worker_last_seen[worker_name] = datetime.datetime.now() # Reset for demo
                return False, self.worker_last_seen[worker_name] - datetime.timedelta(seconds=650)
            else:
                return True, datetime.datetime.now()
        else:
            return True, datetime.datetime.now()

    def check_queues_health(self):
        """
        Checks the health of all configured notification queues.
        """
        logging.info("--- Checking Notification Queue Health ---")
        all_queues_healthy = True
        for queue_name in self.queue_names:
            backlog_size, is_healthy = self._get_queue_status(queue_name)
            if backlog_size > self.max_queue_backlog or not is_healthy:
                logging.error(f"Queue '{queue_name}' is UNHEALTHY. Backlog: {backlog_size}, Healthy Status: {is_healthy}")
                all_queues_healthy = False
            else:
                logging.info(f"Queue '{queue_name}' is HEALTHY. Backlog: {backlog_size}")
        return all_queues_healthy

    def check_workers_health(self):
        """
        Checks the health of all configured notification workers.
        """
        logging.info("--- Checking Notification Worker Health ---")
        all_workers_healthy = True
        for worker_name in self.worker_names:
            is_running, last_heartbeat = self._get_worker_status(worker_name)
            time_since_heartbeat = (datetime.datetime.now() - last_heartbeat).total_seconds()

            if not is_running:
                logging.error(f"Worker '{worker_name}' is DOWN.")
                all_workers_healthy = False
            elif time_since_heartbeat > self.max_worker_downtime_seconds:
                logging.warning(f"Worker '{worker_name}' is UNHEALTHY. No heartbeat in {time_since_heartbeat:.2f} seconds.")
                all_workers_healthy = False
            else:
                logging.info(f"Worker '{worker_name}' is HEALTHY. Last heartbeat: {time_since_heartbeat:.2f} seconds ago.")

        return all_workers_healthy

    def run_all_health_checks(self):
        """
        Runs all health checks for queues and workers.
        """\n        logging.info("\n=== Running ALL Notification Service Health Checks ===")
        queues_healthy = self.check_queues_health()
        workers_healthy = self.check_workers_health()
        total_healthy = queues_healthy and workers_healthy

        if total_healthy:
            logging.info("Notification service is operating NORMALLY.")
        else:
            logging.error("Notification service has detected ISSUES.")
        return total_healthy

if __name__ == "__main__":
    # Example usage
    queue_names = ["email-queue-critical", "email-queue-marketing", "inapp-queue-priority", "inapp-queue-general"]
    worker_names = ["email-worker-1", "email-worker-2", "inapp-worker-1", "inapp-worker-2"]

    health_checker = NotificationHealthChecker(queue_names, worker_names, max_queue_backlog=100, max_worker_downtime_seconds=300)

    # Simulate some time passing to test worker downtime
    # For a real scenario, this would be run periodically by a monitoring system.
    import time
    health_checker.run_all_health_checks()
    print("\nSimulating some time passing...")
    time.sleep(3) # Simulate a short delay
    health_checker.worker_last_seen["email-worker-1"] = datetime.datetime.now() - datetime.timedelta(seconds=700) # Simulate an old heartbeat
    health_checker.run_all_health_checks()

    print("\nSimulating another run...")
    time.sleep(3)
    health_checker.run_all_health_checks()
