import datetime
import logging
import os
import time

import psutil
from prometheus_client import Gauge, start_http_server

# --- Configuration --- #
LOG_FILE = "/var/log/financial_export.log"
PROCESS_NAME = "financial_export_process"  # Replace with the actual process name if different
ALERT_THRESHOLD_SECONDS = 3600  # 1 hour
PROMETHEUS_PORT = 8000

# --- Logging Setup --- #
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# --- Prometheus Metrics --- #
export_duration_seconds = Gauge(
    "financial_export_duration_seconds", "Duration of the financial export process"
)
export_status = Gauge(
    "financial_export_status", "Status of the financial export process (1=success, 0=failure)"
)
query_execution_time_seconds = Gauge(
    "financial_export_query_execution_time_seconds", "Time taken for individual queries"
)
data_transfer_rate_bytes_per_second = Gauge(
    "financial_export_data_transfer_rate_bytes_per_second",
    "Rate of data transfer during export",
)
cpu_utilization_percent = Gauge(
    "node_cpu_utilization_percent", "Current CPU utilization in percentage"
)
memory_utilization_percent = Gauge(
    "node_memory_utilization_percent", "Current memory utilization in percentage"
)
disk_io_read_bytes_total = Gauge(
    "node_disk_io_read_bytes_total", "Total bytes read from disk"
)
disk_io_write_bytes_total = Gauge(
    "node_disk_io_write_bytes_total", "Total bytes written to disk"
)
network_bytes_sent_total = Gauge(
    "node_network_bytes_sent_total", "Total bytes sent over the network"
)
network_bytes_recv_total = Gauge(
    "node_network_bytes_recv_total", "Total bytes received over the network"
)


def monitor_resources(process_name: str):
    """Monitors CPU, memory, disk I/O, and network utilization."""
    logging.info("Starting resource monitoring...")
    start_disk_io = psutil.disk_io_counters()
    start_net_io = psutil.net_io_counters()

    while True:
        # System-wide metrics (can be filtered by process if needed dynamically)
        cpu_utilization_percent.set(psutil.cpu_percent(interval=1))
        memory_utilization_percent.set(psutil.virtual_memory().percent)

        current_disk_io = psutil.disk_io_counters()
        disk_io_read_bytes_total.set(current_disk_io.read_bytes - start_disk_io.read_bytes)
        disk_io_write_bytes_total.set(
            current_disk_io.write_bytes - start_disk_io.write_bytes
        )

        current_net_io = psutil.net_io_counters()
        network_bytes_sent_total.set(current_net_io.bytes_sent - start_net_io.bytes_sent)
        network_bytes_recv_total.set(current_net_io.bytes_recv - start_net_io.bytes_recv)

        PIDs = filter(lambda p: p.info["name"] == process_name, psutil.process_iter(["pid", "name"]))
        for proc in PIDs:
            try:
                p = psutil.Process(proc.info["pid"])
                logging.info(
                    f"Process {process_name} (PID: {p.pid}) - CPU: {p.cpu_percent(interval=None)}%," # interval calculates since last call
                    f" Memory: {p.memory_percent():.2f}%"
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                logging.warning(f"Could not access process {proc.info['pid']} details.")

        time.sleep(60)  # Monitor every 60 seconds


def record_query_metric(query_name: str, duration: float):
    """Records the execution time of a specific query."""
    query_execution_time_seconds.set(duration)
    logging.info(f"Query '{query_name}' executed in {duration:.4f} seconds.")


def record_data_transfer_metric(batch_size_bytes: int, duration: float):
    """Records the data transfer rate for a batch."""
    if duration > 0:
        rate = batch_size_bytes / duration
        data_transfer_rate_bytes_per_second.set(rate)
        logging.info(f"Data transfer rate: {rate:.2f} bytes/second.")


def export_process_wrapper(func):
    """Decorator to wrap the financial export process for logging and metrics."""

    def wrapper(*args, **kwargs):
        logging.info("Financial export process started.")
        start_time = time.time()
        export_status.set(0)  # Assume failure initially
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            export_duration_seconds.set(duration)
            export_status.set(1)  # Success
            logging.info("Financial export process completed successfully.")
            logging.info(f"Total export duration: {duration:.2f} seconds.")

            if duration > ALERT_THRESHOLD_SECONDS:
                logging.warning(
                    f"Financial export duration ({duration:.2f}s) exceeded "
                    f"threshold ({ALERT_THRESHOLD_SECONDS}s)."
                )
            return result
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            export_duration_seconds.set(duration)
            export_status.set(0)  # Failure
            logging.error(f"Financial export process failed: {e}", exc_info=True)
            logging.info(f"Total export duration before failure: {duration:.2f} seconds.")
            raise

    return wrapper


@export_process_wrapper
def financial_export_process(*args, **kwargs):
    """This is a placeholder for your actual financial export logic."""
    logging.info("Simulating financial export steps...")

    # Example: Simulate a long-running query
    query_start = time.time()
    time.sleep(10)  # Simulate database query
    query_end = time.time()
    record_query_metric("main_data_query", query_end - query_start)

    # Example: Simulate batch processing and data transfer
    total_records = 100000
    batch_size = 10000
    for i in range(0, total_records, batch_size):
        batch_start_time = time.time()
        logging.info(f"Processing batch {int(i/batch_size) + 1}/ "
                     f"{int(total_records/batch_size)}...")
        time.sleep(2)  # Simulate data processing/transfer for a batch
        batch_end_time = time.time()
        batch_duration = batch_end_time - batch_start_time
        record_data_transfer_metric(batch_size * 100, batch_duration) # Assume 100 bytes/record

    logging.info("Simulated export complete.")
    # Example of potential error
    # if datetime.datetime.now().hour == 23: # Simulate failure condition
    #     raise ValueError("Simulated error: Export cannot complete at this hour!")


def main():
    logging.info("Starting Prometheus HTTP server...")
    start_http_server(PROMETHEUS_PORT)

    logging.info("Starting financial export process...")
    try:
        # Run the financial export process
        financial_export_process()
    except Exception as e:
        logging.error(f"Main export process encountered an unhandled error: {e}")

    # Keep resource monitoring alive indefinitely for now
    # In a real scenario, this might be split into a separate process or a daemon
    # or integrated with a systemd service that manages both the exporter and the monitor
    # For this example, we'll just run it for a long duration.
    try:
        monitor_resources(PROCESS_NAME)
    except KeyboardInterrupt:
        logging.info("Resource monitoring stopped.")


if __name__ == "__main__":
    main()
