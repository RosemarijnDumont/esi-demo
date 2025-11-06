
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from functools import lru_cache

from app.core.database import get_db_connection, get_read_replica_connection
from app.models.financial_transaction import FinancialTransaction

logger = logging.getLogger(__name__)


class FinancialDataRepository:
    def __init__(self):
        pass

    def get_financial_transactions_in_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        limit: int,
        offset: int,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves financial transactions within a specified date range with pagination.
        Uses a read-replica for export operations.
        """
        try:
            with get_read_replica_connection() as conn:
                with conn.cursor() as cursor:
                    query = """
                        SELECT
                            id,
                            transaction_date,
                            amount,
                            currency,
                            description,
                            category,
                            account_id,
                            created_at,
                            updated_at,
                            metadata
                        FROM financial_transactions
                        WHERE transaction_date BETWEEN %s AND %s
                        ORDER BY transaction_date, id
                        LIMIT %s OFFSET %s;
                    """
                    cursor.execute(query, (start_date, end_date, limit, offset))
                    columns = [desc[0] for desc in cursor.description]
                    transactions = []
                    for row in cursor.fetchall():
                        transactions.append(dict(zip(columns, row)))
                    logger.debug(f"Fetched {len(transactions)} transactions from DB for {start_date}-{end_date} offset {offset}")
                    return transactions
        except Exception as e:
            logger.error(f"Error fetching financial transactions: {e}")
            raise

    @lru_cache(maxsize=128)  # Cache up to 128 different categories
    def get_transaction_category_name(self, category_id: int) -> Optional[str]:
        """
        Retrieves the name of a transaction category by its ID, using caching.
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query = "SELECT name FROM transaction_categories WHERE id = %s;"
                    cursor.execute(query, (category_id,))
                    result = cursor.fetchone()
                    return result[0] if result else None
        except Exception as e:
            logger.error(f"Error fetching transaction category name for ID {category_id}: {e}")
            return None

    # Example of a potentially inefficient query identified and refactored
    # Original (hypothetical inefficient query):
    # SELECT * FROM financial_transactions WHERE EXTRACT(QUARTER FROM transaction_date) = %s AND EXTRACT(YEAR FROM transaction_date) = %s;
    # This forces a full table scan and prevents index usage on transaction_date.
    # Refactored to use BETWEEN for date ranges, allowing index usage.

    # Ensure appropriate indexes are in place for performance
    # Example SQL for index creation (to be run as part of migrations):
    # CREATE INDEX idx_financial_transactions_date ON financial_transactions (transaction_date);
    # CREATE INDEX idx_financial_transactions_category_id ON financial_transactions (category_id);

