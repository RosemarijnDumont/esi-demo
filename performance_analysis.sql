-- SQL queries to analyze dashboard query performance

-- 1. Identify slow queries (example for PostgreSQL, adapt for other DBs)
SELECT
  query,
  total_time,
  calls,
  mean_time,
  max_time
FROM pg_stat_statements
WHERE query ILIKE '%dashboard%'
ORDER BY total_time DESC
LIMIT 10;

-- 2. Analyze a specific slow query using EXPLAIN ANALYZE (replace your_slow_query_here with an actual slow query)
EXPLAIN ANALYZE
SELECT
  -- your_columns
FROM
  your_tables
WHERE
  -- your_conditions;

-- 3. Check for missing indexes on frequently filtered or joined columns
-- (Example for PostgreSQL, adapt for other DBs)
SELECT
  relname AS table_name,
  idx.indrelid :: REGCLASS :: TEXT AS table_with_no_index,
  pg_size_pretty(pg_relation_size(relid)) AS table_size,
  pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_stat_user_tables AS p,
  pg_class AS idx
WHERE
  NOT EXISTS (
    SELECT
      1
    FROM pg_index i
    WHERE
      i.indrelid = idx.oid
  )
  AND idx.relkind = ANY (ARRAY ['r', 'm'])
ORDER BY
  pg_relation_size(relid) DESC;

-- 4. Get index usage statistics (PostgreSQL example)
SELECT
  relname AS table_name,
  indexrelname AS index_name,
  idx_scan AS index_scans_count,
  idx_tup_read AS index_tuples_read,
  idx_tup_fetch AS index_tuples_fetched
FROM pg_stat_user_indexes
ORDER BY
  idx_scan DESC;
