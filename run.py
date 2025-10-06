from notification_service.app import app
from notification_service.core.scheduler import Scheduler
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    # Start the scheduler in the main process. In a production Flask app with Gunicorn/uWSGI,
    # you might want to run the scheduler in a separate dedicated worker process (e.g., using Celery).
    # For this example, we'll start it here.
    logging.info("Starting Notification Service Scheduler...")
    Scheduler.start()

    logging.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=5001, debug=True)
