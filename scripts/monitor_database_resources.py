import psycopg2
import time
import os
from datetime import datetime

# --- Configuration Parameters ---
pG_HOST = os.getenv("PG_HOST", "localhost")
pG_DATABASE = os.getenv("PG_DATABASE", "your_database_name")
pG_USER = os.getenv("PG_USER", "your_username")
pG_PASSWORD = os.getenv("PG_PASSWORD", "your_password")
PG_PORT = os.getenv("PG_PORT", "5432")

MONITOR_INTERVAL_SECONDS = 10 # How often to poll the database
MONITOR_DURATION_SECONDS = 3600 # Total duration to monitor (e.g., 1 hour for export)
OUTPUT_LOG_FILE = "database_monitoring_log.txt"

# --- SQL Queries to Monitor ---
# Using the SQL queries from `sql/02_monitor_db_performance.sql`

SQL_ACTIVE_QUERIES = """
SELECT
    pid,
    datname,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    query
FROM
    pg_stat_activity
WHERE
    state = 'active'
ORDER BY
    query_start ASC;
"""

SQL_BLOCKED_QUERIES = """
SELECT
    a.pid AS blocked_pid,
    a.usename AS blocked_user,
    a.query AS blocked_query,
    b.pid AS blocking_pid,
    b.usename AS blocking_user,
    b.query AS blocking_query
FROM
    pg_stat_activity a
JOIN
    pg_locks dep_locks ON a.pid = dep_locks.pid AND dep_locks.granted = FALSE
JOIN
    pg_locks pg_dep_lock_info ON dep_locks.locktype = pg_dep_lock_info.locktype
    AND dep_locks.database IS NOT DISTINCT FROM pg_dep_lock_info.database
    AND dep_locks.relation IS NOT DISTINCT FROM pg_dep_lock_info.relation
    AND dep_locks.page IS NOT DISTINCT FROM pg_dep_lock_info.page
    AND dep_locks.tuple IS NOT DISTINCT FROM pg_dep_lock_info.tuple
    AND dep_locks.transactionid IS NOT DISTINCT FROM pg_dep_lock_info.transactionid
    AND dep_lock_info.classid IS NOT DISTINCT FROM pg_lock_info.classid
    AND dep_locks.objid IS NOT DISTINCT FROM pg_dep_lock_info.objid
    AND dep_locks.objsubid IS NOT DISTINCT FROM pg_dep_lock_info.objsubid
    AND pg_dep_lock_info.granted = TRUE
    AND a.pid != pg_dep_lock_info.pid
JOIN
    pg_stat_activity b ON pg_dep_lock_info.pid = b.pid
WHERE
    a.wait_event_type = 'Lock';
"""

SQL_IO_PER_TABLE = """
SELECT
    relname AS table_name,
    schemaname AS schema_name,
    heap_blks_read + idx_blks_read + toast_blks_read + tib_blks_read AS total_blocks_read,
    heap_blks_hit + idx_blks_hit + toast_blks_hit + tib_blks_hit AS total_blocks_hit,
    (heap_blks_hit + idx_blks_hit + toast_blks_hit + tib_blks_hit) * 100 / NULLIF( (heap_blks_read + idx_blks_read + toast_blks_read + tib_blks_read), 0) AS cache_hit_ratio_percent
FROM
    pg_statio_all_tables
ORDER BY
    total_blocks_read DESC
LIMIT 10;
"""

SQL_TEMP_FILE_USAGE = """
SELECT
    datname,
    temp_files AS total_temp_files,
    temp_bytes AS total_temp_bytes
FROM
    pg_stat_database
ORDER BY
    temp_bytes DESC;
"""

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=PG_HOST,
        database=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        port=PG_PORT
    )

def log_data(file_path, header, data):
    """Writes queried data to a log file."""
    with open(file_path, "a") as f:
        f.write(f"\n--- {header} ({datetime.now().isoformat()}) ---\n")
        if data:
            # Write column headers
            f.write("| " + " | ".join(data[0].keys()) + " |\n")
            f.write("|-" + "-|-".join(["-" * len(str(k)) for k in data[0].keys()]) + "-|\n")
            # Write rows
            for row in data:
                f.write("| " + " | ".join([str(v) for v in row.values()]) + " |\n")
        else:
            f.write("No data found.\n")

def run_monitoring():
    """
    Main function to run the database monitoring process.
    Connects to the DB, executes monitoring queries, and logs the results.
    """
    print(f"Starting database monitoring for {MONITOR_DURATION_SECONDS} seconds...")
    print(f"Output will be logged to {OUTPUT_LOG_FILE}")

    start_time = time.time()

    with open(OUTPUT_LOG_FILE, "w") as f:
        f.write(f"Database Monitoring Started: {datetime.now().isoformat()}\n")
        f.write(f"Monitoring DB: {PG_DATABASE} on {PG_HOST}:{PG_PORT}\n")
        f.write(f"Monitoring Interval: {MONITOR_INTERVAL_SECONDS} seconds\n")
        f.write(f"Total Monitoring Duration: {MONITOR_DURATION_SECONDS} seconds\n\n")

    try:
        while (time.time() - start_time) < MONITOR_DURATION_SECONDS:
            conn = None # Initialize conn to None for error handling
            try:
                conn = get_db_connection()
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                # Monitor Active Queries
                cur.execute(SQL_ACTIVE_QUERIES)
                active_queries = cur.fetchall()
                log_data(OUTPUT_LOG_FILE, "Active Queries", active_queries)

                # Monitor Blocked Queries
                cur.execute(SQL_BLOCKED_QUERIES)
                blocked_queries = cur.fetchall()
                log_data(OUTPUT_LOG_FILE, "Blocked Queries", blocked_queries)
                if blocked_queries:
                    print(f"!!! WARNING: Blocked queries detected at {datetime.now().isoformat()} !!!")

                # Monitor I/O Per Table
                cur.execute(SQL_IO_PER_TABLE)
                io_per_table = cur.fetchall()
                log_data(OUTPUT_LOG_FILE, "I/O Per Table (Top 10)", io_per_table)

                # Monitor Temporary File Usage
                cur.execute(SQL_TEMP_FILE_USAGE)
                temp_file_usage = cur.fetchall()
                log_data(OUTPUT_LOG_FILE, "Temporary File Usage", temp_file_usage)

                cur.close()
                conn.close()

            except psycopg2.Error as e:
                print(f"Database error at {datetime.now().isoformat()}: {e}")
                if conn:
                    conn.close()
            except Exception as e:
                print(f"An unexpected error occurred at {datetime.now().isoformat()}: {e}")
                if conn:
                    conn.close()

            print(f"Monitoring iteration complete. Next poll in {MONITOR_INTERVAL_SECONDS} seconds...")
            time.sleep(MONITOR_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    finally:
        end_time = datetime.now().isoformat()
        with open(OUTPUT_LOG_FILE, "a") as f:
            f.write(f"\nDatabase Monitoring Finished: {end_time}\n")
        print(f"Database monitoring completed. Results are in {OUTPUT_LOG_FILE}")

if __name__ == "__main__":
    # Install psycopg2-binary: pip install psycopg2-binary
    # Set environment variables or update the script with your DB credentials:
    # PG_HOST, PG_DATABASE, PG_USER, PG_PASSWORD, PG_PORT

    # Example usage (uncomment and replace with actual values if not using env vars):
    # os.environ["PG_DATABASE"] = "your_financial_db"
    # os.environ["PG_USER"] = "dbuser"
    # os.environ["PG_PASSWORD"] = "dbpass"

    if not all([PG_HOST, PG_DATABASE, PG_USER, PG_PASSWORD, PG_PORT]):
        print("WARNING: Database credentials are not fully set via environment variables or script.")
        print("Please configure PG_HOST, PG_DATABASE, PG_USER, PG_PASSWORD, and PG_PORT.")
        exit(1)

    try:
        import psycopg2.extras # Required for DictCursor
    except ImportError:
        print("Error: psycopg2-binary library not found.")
        print("Please install it using: pip install psycopg2-binary")
        exit(1)

    run_monitoring()