
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends, status
from typing import Dict, Any
from uuid import uuid4
import logging

from app.services.financial_export_service import FinancialExportService
from app.core.celery_app import celery_app

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Financial Export API",
    description="API for triggering and monitoring long-running financial export processes.",
    version="1.0.0"
)

def get_financial_export_service():
    return FinancialExportService()


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint to ensure the API is running."""
    return {"status": "200 OK", "message": "API is healthy"}


@app.post("/export", status_code=status.HTTP_202_ACCEPTED)
async def trigger_financial_export(
    quarter: str,
    year: int,
    service: FinancialExportService = Depends(get_financial_export_service)
) -> Dict[str, str]:
    """
    Triggers an asynchronous financial data export for a given quarter and year.
    The export process runs as a background task using Celery.
    """
    task_id = str(uuid4())
    logger.info(f"API: Triggering financial export for {quarter} {year} with task ID: {task_id}")

    # Enqueue the Celery task
    service.export_financial_data_task.delay(task_id, quarter, year)

    return {
        "task_id": task_id,
        "status": "Export process initiated",
        "message": "You can check the status of the export using the /export/status/{task_id} endpoint."
    }


@app.get("/export/status/{task_id}", response_model=Dict[str, Any])
async def get_export_status(
    task_id: str,
    service: FinancialExportService = Depends(get_financial_export_service)
) -> Dict[str, Any]:
    """
    Retrieves the current status of a financial export task.
    """
    logger.info(f"API: Checking status for task ID: {task_id}")
    status_info = service.get_export_status(task_id)

    if status_info['status'] == 'PENDING' and 'message' in status_info and status_info['message'] == 'Unknown task state.':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or has not started yet.")

    return status_info

