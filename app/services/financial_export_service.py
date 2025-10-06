import logging
import pandas as pd
from sqlalchemy import create_engine, text
from tenacity import retry, stop_after_attempt, wait_fixed, before_log, after_log

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinancialExportService:
    def __init__(self, db_connection_string):
        self.engine = create_engine(db_connection_string)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(60),
        before=before_log(logger, logging.INFO),
        after=after_log(logger, logging.INFO),
        reraise=True
    )
    def _execute_query(self, query, params=None):
        """Executes a given SQL query with retry mechanism."""
        with self.engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            return pd.DataFrame(result.fetchall(), columns=result.keys())

    def get_financial_data(self, quarter, year):
        """Retrieves financial data for a specific quarter and year."""
        logger.info(f"Attempting to retrieve financial data for Q{quarter} {year}")
        # Optimized query with potential for materialized view or indexed columns
        query = f"""
            SELECT
                t.transaction_id,
                t.amount,
                t.currency,
                t.transaction_date,
                t.description,
                a.account_name,
                a.account_type,
                l.legal_entity_name,
                p.product_name
            FROM
                transactions t
            JOIN
                accounts a ON t.account_id = a.account_id
            JOIN
                legal_entities l ON t.legal_entity_id = l.legal_entity_id
            LEFT JOIN
                products p ON t.product_id = p.product_id
            WHERE
                EXTRACT(QUARTER FROM t.transaction_date) = :quarter AND
                EXTRACT(YEAR FROM t.transaction_date) = :year
            ORDER BY
                t.transaction_date ASC
        """
        params = {'quarter': quarter, 'year': year}
        df = self._execute_query(query, params)
        logger.info(f"Retrieved {len(df)} financial records for Q{quarter} {year}")
        return df

    def validate_data(self, actual_df):
        """Basic data validation to ensure completeness and accuracy."""
        if actual_df.empty:
            logger.warning("Exported DataFrame is empty.")
            return False
        # Example validation: Check for nulls in critical columns
        if actual_df[['transaction_id', 'amount', 'transaction_date', 'account_name']].isnull().any().any():
            logger.error("Critical columns contain NULL values.")
            return False
        # Add more sophisticated validation logic here (e.g., sum checks, row counts against source)
        logger.info("Data validation passed.")
        return True

    def export_to_csv(self, dataframe, filepath):
        """Exports a pandas DataFrame to a CSV file."""
        try:
            dataframe.to_csv(filepath, index=False)
            logger.info(f"Successfully exported data to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error exporting data to CSV at {filepath}: {e}")
            return False

