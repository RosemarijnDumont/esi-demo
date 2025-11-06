-- File: docs/data_volume_assessment.md
-- Description: Guide for assessing the growth rate and total volume of financial data tables.

# Data Volume Assessment for Financial Export

This document outlines the steps to assess the growth rate and total volume of financial data tables relevant to the export process. Understanding data volume trends is crucial for anticipating performance issues and planning necessary optimizations.

## 1. Identify Key Financial Tables

First, identify all tables that are part of the financial export query or are otherwise critical for the export process. Common examples include:

*   `financial_ledger_accounts` (e.g., individual transactions)
*   `financial_general_accounts` (e.g., chart of accounts)
*   `financial_journals`
*   `financial_transactions`
*   `financial_periods`
*   `financial_categories`
*   Any related dimension or fact tables used in reporting.

## 2. SQL Queries for Current Table Sizes

Use the following SQL queries (adapt for your specific database system, e.g., PostgreSQL, MySQL, SQL Server) to get the current size and row counts for your identified tables.

### PostgreSQL Example:

```sql
SELECT
    relname AS table_name,
    pg_size_pretty(pg_total_relation_size(oid)) AS total_size_with_indexes,
    pg_relation_size(oid) AS table_data_size_bytes,
    reltuples AS row_count
FROM
    pg_class
WHERE
    relname IN ('financial_ledger_accounts', 'financial_general_accounts', 'financial_transactions') -- Add your table names here
    AND relkind = 'r'
ORDER BY
    pg_total_relation_size(oid) DESC;

-- To get statistics for all tables (if you need to identify large tables generally)
SELECT
    relname AS table_name,
    pg_size_pretty(pg_total_relation_size(oid)) AS total_size_with_indexes,
    reltuples AS row_count
FROM
    pg_class
WHERE
    relkind = 'r'
ORDER BY
    pg_total_relation_size(oid) DESC
LIMIT 20;
```

### MySQL Example:

```sql
SELECT
    table_name AS table_name,
    table_rows AS row_count,
    data_length AS table_data_size_bytes,
    index_length AS index_size_bytes,
    (data_length + index_length) AS total_size_bytes,
    (data_length + index_length) / 1024 / 1024 AS total_size_mb
FROM
    information_schema.tables
WHERE
    table_schema = 'your_database_name' AND table_name IN ('financial_ledger_accounts', 'financial_general_accounts'); -- Add your table names here

```

### SQL Server Example:

```sql
SELECT
    t.NAME AS TableName,
    s.Name AS SchemaName,
    p.rows AS RowCounts,
    SUM(a.total_pages) * 8 AS TotalSpaceKB,
    CAST(ROUND(((SUM(a.total_pages) * 8) / 1024.00), 2) AS NUMERIC(36, 2)) AS TotalSpaceMB,
    SUM(a.used_pages) * 8 AS UsedSpaceKB,
    CAST(ROUND(((SUM(a.used_pages) * 8) / 1024.00), 2) AS NUMERIC(36, 2)) AS UsedSpaceMB,
    (SUM(a.total_pages) - SUM(a.used_pages)) * 8 AS UnusedSpaceKB,
    CAST(ROUND(((SUM(a.total_pages) - SUM(a.used_pages)) * 8) / 1024.00, 2) AS NUMERIC(36, 2)) AS UnusedSpaceMB
FROM
    sys.tables t
INNER JOIN
    sys.indexes i ON t.Object_ID = i.Object_ID
INNER JOIN
    sys.partitions p ON i.Object_ID = p.Object_ID AND i.index_id = p.index_id
INNER JOIN
    sys.allocation_units a ON p.partition_id = a.container_id
LEFT OUTER JOIN
    sys.schemas s ON t.schema_id = s.schema_id
WHERE
    t.NAME IN ('financial_ledger_accounts', 'financial_general_accounts') -- Add your table names here
    AND t.is_ms_shipped = 0
    AND i.Object_ID > 255
GROUP BY
    t.Name, s.Name, p.Rows
ORDER BY
    TotalSpaceMB DESC;
```

## 3. Historical Data Collection

To assess growth rate, you need historical snapshots of these metrics. Ideally, you should have data from several previous quarters (e.g., last 4-8 quarters).

If historical snapshotting is not in place, you may need to:

1.  **Run the above queries regularly:** Schedule a job to run these queries quarterly (or monthly) and store the results in a separate monitoring database or log files.
2.  **Estimate using date-partitioned data:** If your tables are partitioned or have a `created_at` / `transaction_date` column, you can query row counts and sizes for specific date ranges.

    Example (PostgreSQL for `financial_ledger_accounts` by quarter):

    ```sql
    SELECT
        TO_CHAR(transaction_date, 'YYYY-Q') AS year_quarter,
        COUNT(*) AS row_count,
        pg_size_pretty(SUM(pg_column_size(CAST(t.* AS text)))) AS estimated_quarter_size_text -- Rough estimate
    FROM
        financial_ledger_accounts t
    GROUP BY
        year_quarter
    ORDER BY
        year_quarter;
    ```

    *Note: `SUM(pg_column_size(CAST(t.* AS text)))` is a very rough estimate and should be used with caution. Direct table size functions are more accurate.*

## 4. Analysis

Once you have current and historical data:

*   **Calculate Quarterly Growth:** Determine the percentage increase in row count and total size for each key table quarter-over-quarter.
*   **Identify Fast-Growing Tables:** Pinpoint tables exhibiting significant growth, as these are most likely to contribute to future performance issues.
*   **Relate to Export Performance:** Compare data growth trends with the onset and worsening of export timeouts. Increased data volume directly impacts query execution time and I/O.
*   **Project Future Volumes:** Based on growth rates, project data volumes for the next 1-2 years to proactively plan for scaling, archiving, or partitioning strategies.

## 5. Stored Procedures/ORM Calls Profiling

If the export uses stored procedures or ORM, profiling becomes crucial.

*   **Stored Procedures:** If there are stored procedures involved, use database-specific tools to profile their execution. For PostgreSQL, `pg_stat_statements` (if enabled) can offer insights into frequently executed queries within procedures.
    *   Enable `pg_stat_statements` by adding `pg_stat_statements` to `shared_preload_libraries` in `postgresql.conf` and `CREATE EXTENSION pg_stat_statements;` in your DB.
    *   Query `pg_stat_statements`:
        ```sql
        SELECT
            query,
            calls,
            total_time,
            mean_time,
            min_time,
            max_time,
            rows
        FROM
            pg_stat_statements
        ORDER BY
            total_time DESC
        LIMIT 20;
        ```
*   **ORM Calls:**
    *   Enable SQL logging in your ORM (e.g., SQLAlchemy, Django ORM, Hibernate). This will show the actual SQL queries generated and their execution times.
    *   Use application-level profilers (e.g., cProfile for Python, VisualVM for Java) to identify slow points in the application code that interact with the ORM.
    *   Review `EXPLAIN ANALYZE` output for the specific queries generated by the ORM (as in `sql/01_analyze_export_queries.sql`).

This comprehensive assessment will provide a clear picture of the data landscape and its impact on the financial export process, guiding subsequent optimization efforts.