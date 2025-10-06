-- Recommended indexes based on the optimized query in financial_export_service.py

-- Index on transaction_date for efficient filtering by quarter and year
CREATE INDEX IF NOT EXISTS idx_transactions_transaction_date ON transactions (transaction_date);

-- Index on account_id for joins with the accounts table
CREATE INDEX IF NOT EXISTS idx_transactions_account_id ON transactions (account_id);

-- Index on legal_entity_id for joins with the legal_entities table
CREATE INDEX IF NOT EXISTS idx_transactions_legal_entity_id ON transactions (legal_entity_id);

-- Index on product_id for joins with the products table (if product_id is frequently used in WHERE clauses or joins)
CREATE INDEX IF NOT EXISTS idx_transactions_product_id ON transactions (product_id);

-- Composite index for transaction_date, account_id, legal_entity_id if these are often queried together
-- CREATE INDEX IF NOT EXISTS idx_transactions_date_account_entity ON transactions (transaction_date, account_id, legal_entity_id);


-- Optional: Materialized View for frequently accessed aggregated financial data
-- This can pre-calculate and store the results of complex queries, reducing query time significantly.
-- You would need a mechanism to refresh this materialized view periodically (e.g., daily, weekly, or before quarterly exports).

-- Example Materialized View (adjust columns and aggregations as per actual reporting needs)
/*
CREATE MATERIALIZED VIEW mv_quarterly_financial_summary AS
SELECT
    EXTRACT(QUARTER FROM t.transaction_date) AS qtr,
    EXTRACT(YEAR FROM t.transaction_date) AS yr,
    a.account_name,
    l.legal_entity_name,
    SUM(t.amount) AS total_amount,
    COUNT(t.transaction_id) AS total_transactions
FROM
    transactions t
JOIN
    accounts a ON t.account_id = a.account_id
JOIN
    legal_entities l ON t.legal_entity_id = l.legal_entity_id
GROUP BY
    qtr, yr, a.account_name, l.legal_entity_name
ORDER BY
    yr, qtr, a.account_name;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_quarterly_financial_summary_unique ON mv_quarterly_financial_summary (qtr, yr, account_name, legal_entity_name);

-- To refresh the materialized view (run this periodically):
-- REFRESH MATERIALIZED VIEW mv_quarterly_financial_summary;
*/

-- Existing table schemas (provided for context, assume these exist)
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    account_id INT NOT NULL,
    legal_entity_id INT NOT NULL,
    product_id INT,
    amount DECIMAL(18, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    transaction_date DATE NOT NULL,
    description TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (legal_entity_id) REFERENCES legal_entities(legal_entity_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id SERIAL PRIMARY KEY,
    account_name VARCHAR(255) NOT NULL,
    account_type VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS legal_entities (
    legal_entity_id SERIAL PRIMARY KEY,
    legal_entity_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL
);
