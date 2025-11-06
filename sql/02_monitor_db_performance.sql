-- File: sql/02_monitor_db_performance.sql
-- Description: SQL queries to monitor database performance during an attempted export.
-- This script focuses on identifying locking, slow I/O, or resource contention in PostgreSQL.

-- 1. Identify active queries and their states (to find long-running or blocked queries)
SELECT
    pid,
    datname,
    usename,
    application_name,
    client_addr,
    backend_start,
    state,
    state_change,
    wait_event_type,
    wait_event,
    query_start,
    xact_start,
    query,
    backend_type
FROM
    pg_stat_activity
WHERE
    state = 'active'
ORDER BY
    query_start ASC;

-- 2. Identify blocked queries (if any transactions are holding locks)
SELECT
    a.pid AS blocked_pid,
    a.usename AS blocked_user,
    a.application_name AS blocked_application,
    a.client_addr AS blocked_client,
    a.query_start AS blocked_query_start,
    a.query AS blocked_query,
    b.pid AS blocking_pid,
    b.usename AS blocking_user,
    b.application_name AS blocking_application,
    b.client_addr AS blocking_client,
    b.query_start AS blocking_query_start,
    b.query AS blocking_query,
    pg_dep_lock_info.mode AS lock_mode,
    pg_dep_lock_info.locktype AS lock_type,
    pg_dep_lock_info.granted AS lock_granted
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
    AND dep_locks.classid IS NOT DISTINCT FROM pg_dep_lock_info.classid
    AND dep_locks.objid IS NOT DISTINCT FROM pg_dep_lock_info.objid
    AND dep_locks.objsubid IS NOT DISTINCT FROM pg_dep_lock_info.objsubid
    AND pg_dep_lock_info.granted = TRUE
    AND a.pid != pg_dep_lock_info.pid
JOIN
    pg_stat_activity b ON pg_dep_lock_info.pid = b.pid
WHERE
    a.wait_event_type = 'Lock';

-- 3. Monitor I/O usage per table (PostgreSQL 9.2+)
-- This provides insights into which tables are experiencing the most I/O activity.
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
LIMIT 20;

-- 4. Monitor Temporary File Usage (indicates queries that spill to disk due to memory limits)
SELECT
    datname, 
    temp_files AS total_temp_files,
    temp_bytes AS total_temp_bytes
FROM 
    pg_stat_database
ORDER BY
    temp_bytes DESC;

-- 5. Track database size and table sizes over time (useful for trend analysis)
SELECT
    NOW() AS collection_time,
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS database_size
FROM
    pg_database
ORDER BY
pg_database_size(pg_database.datname) DESC;

-- Get sizes of top N tables in the current database
SELECT
    NOW() AS collection_time,
    relname AS table_name,
    pg_size_pretty(pg_relation_size(oid)) AS table_size,
    pg_size_pretty(pg_total_relation_size(oid)) AS total_table_size_with_indexes
FROM
    pg_class
WHERE
    relkind = 'r'
ORDER BY
    pg_relation_size(oid) DESC
LIMIT 20;

-- How to use:
-- 1. Start the financial export process.
-- 2. While the export is running, repeatedly execute these queries (e.g., every 5-10 seconds)
--    in a separate database client session.
-- 3. Look for:
--    - Long-running queries (from pg_stat_activity) that correspond to the export.
--    - Any blocked queries, and identify the blocking PID and query.
--    - Tables with high `total_blocks_read` and low `cache_hit_ratio_percent` in `pg_statio_all_tables`,
--      indicating potential I/O bottlenecks.
--    - Significant `temp_files` or `temp_bytes` in `pg_stat_database` which could point to
--      memory-intensive sort/hash operations spilling to disk.