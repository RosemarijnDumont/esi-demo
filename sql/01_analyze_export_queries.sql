-- File: sql/01_analyze_export_queries.sql
-- Description: Analyze current financial export SQL queries using EXPLAIN ANALYZE to identify bottlenecks.

-- IMPORTANT: Replace `your_financial_export_query_here` with the actual SQL query
-- used for the financial export. This query should be the exact one causing timeouts.

EXPLAIN (ANALYZE, BUFFERS, WAL, VERBOSE, FORMAT JSON) 
<your_financial_export_query_here>;

-- Example of a complex query that might be part of a financial export:
-- EXPLAIN (ANALYZE, BUFFERS, WAL, VERBOSE, FORMAT JSON)
-- SELECT
--     fla.transaction_id,
--     fla.transaction_date,
--     fla.amount,
--     fla.currency,
--     fla.description,
--     fla.account_id,
--     fga.account_name,
--     fga.account_type,
--     fgt.transaction_type_name,
--     fpe.payee_name,
--     fcat.category_name
-- FROM
--     financial_ledger_accounts fla
-- JOIN
--     financial_general_accounts fga ON fla.account_id = fga.account_id
-- JOIN
--     financial_transaction_types fgt ON fla.transaction_type_id = fgt.transaction_type_id
-- LEFT JOIN
--     financial_payees fpe ON fla.payee_id = fpe.payee_id
-- LEFT JOIN
--     financial_categories fcat ON fla.category_id = fcat.category_id
-- WHERE
--     fla.transaction_date BETWEEN '2023-01-01' AND '2023-03-31'
-- ORDER BY
--     fla.transaction_date, fla.transaction_id;

-- Instructions:
-- 1. Replace `<your_financial_export_query_here>` with the problematic query.
-- 2. Run this script against your database.
-- 3. The output will be a JSON-formatted query plan with execution statistics.
--    Analyze the output for:
--    - High "Total Runtime" values.
--    - Steps with significantly high "actual time" compared to "planning time".
--    - Large "Rows Removed by Filter" which might indicate inefficient WHERE clauses.
--    - Sequential Scans on large tables (index might be missing or not used).
--    - High "Buffers hit" or "Buffers dirtied" indicating I/O-intensive operations.
--    - Locks or anything indicating contention.

-- Consider:
-- - Adding appropriate indexes if sequential scans are prevalent on large tables used in WHERE or JOIN clauses.
-- - Rewriting complex subqueries or common table expressions (CTEs) for better performance.
-- - Optimizing JOIN conditions.
-- - Reducing the amount of data processed by filtering earlier.