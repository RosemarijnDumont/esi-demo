
import logging
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime

from app.core.database import get_db_connection
from app.repositories.financial_data_repository import FinancialDataRepository
from app.core.celery_app import celery_app
from app.core.config import settings

logger = logging.getLogger(__name__)


class FinancialExportService:
    def __init__(self):
        self.repository = FinancialDataRepository()

    @celery_app.task(bind=True, default_retry_delay=300, max_retries=5)
    def export_financial_data_task(self, task_id: str, quarter: str, year: int):
        logger.info(f"Starting financial data export task {task_id} for {quarter} {year}")
        try:
            start_time = datetime.now()
            file_path = self._perform_export(quarter, year)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"Financial export task {task_id} completed in {duration:.2f} seconds. File: {file_path}")
            # In a real application, you'd store file_path in a database associated with task_id
            # and potentially notify the user.
            return {"status": "completed", "file_path": file_path, "duration": duration}
        except Exception as e:
            logger.exception(f"Financial export task {task_id} failed: {e}")
            self.retry(exc=e)

    def _perform_export(self, quarter: str, year: int) -> str:
        # Determine date range for the quarter
        start_date, end_date = self._get_quarter_dates(quarter, year)

        all_data = []
        offset = 0
        limit = settings.EXPORT_BATCH_SIZE

        while True:
            # Fetch data in chunks
            logger.info(f"Fetching financial data from {start_date} to {end_date} with offset {offset} and limit {limit}")
            chunk = self.repository.get_financial_transactions_in_date_range(
                start_date, end_date, limit, offset
            )
            if not chunk:
                break
            all_data.extend(chunk)
            offset += limit
            if len(chunk) < limit:  # Last chunk was smaller than limit, so no more data
                break

        if not all_data:
            logger.warning(f"No financial data found for {quarter} {year}.")
            return "no_data_exported.csv"

        # Convert to pandas DataFrame for easier processing and export
        df = pd.DataFrame(all_data)

        # Example: Add some derived columns or perform light transformations
        df['transaction_month'] = pd.to_datetime(df['transaction_date']).dt.month
        df['transaction_year'] = pd.to_datetime(df['transaction_date']).dt.year

        # Define export path
        export_dir = settings.EXPORT_FILE_DIR
        export_dir.mkdir(parents=True, exist_ok=True)
        file_name = f"financial_export_{year}_{quarter}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        file_path = export_dir / file_name

        # Export to CSV
        df.to_csv(file_path, index=False)
        logger.info(f"Successfully exported {len(df)} records to {file_path}")

        return str(file_path)

    def _get_quarter_dates(self, quarter: str, year: int):
        if quarter == "Q1":
            return datetime(year, 1, 1), datetime(year, 3, 31)
        elif quarter == "Q2":
            return datetime(year, 4, 1), datetime(year, 6, 30)
        elif quarter == "Q3":
            return datetime(year, 7, 1), datetime(year, 9, 30)
        elif quarter == "Q4":
            return datetime(year, 10, 1), datetime(year, 12, 31)
        else:
            raise ValueError(f"Invalid quarter: {quarter}. Must be Q1, Q2, Q3, or Q4.")

    def get_export_status(self, task_id: str) -> Dict[str, Any]:
        task = celery_app.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                'status': task.state,
                'message': 'Export is pending.'
            }
        elif task.state == 'STARTED':
            response = {
                'status': task.state,
                'message': 'Export is in progress.'
            }
        elif task.state == 'SUCCESS':
            response = {
                'status': task.state,
                'message': 'Export completed successfully.',
                'result': task.result
            }
        elif task.state == 'FAILURE':
            response = {
                'status': task.state,
                'message': 'Export failed.',
                'error': str(task.info)
            }
        else:
            response = {
                'status': task.state,
                'message': 'Unknown task state.'
            }
        return response

