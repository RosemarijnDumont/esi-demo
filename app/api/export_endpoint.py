from flask import Blueprint, jsonify, request, send_file
from app.services.financial_export_service import FinancialExportService
import os
import datetime
import logging

financial_export_bp = Blueprint('financial_export', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database connection string - should be loaded from environment variables in a real application
DB_CONNECTION_STRING = os.getenv('DATABASE_URL', 'postgresql://user:password@host:port/database')
EXPORT_DIR = os.getenv('EXPORT_DIR', '/tmp/financial_exports')
os.makedirs(EXPORT_DIR, exist_ok=True)

@financial_export_bp.route('/export/financial', methods=['GET'])
def export_financial_data():
    quarter = request.args.get('quarter', type=int)
    year = request.args.get('year', type=int)

    if not all([quarter, year]):
        return jsonify({"error": "Missing 'quarter' or 'year' parameters"}), 400

    if not (1 <= quarter <= 4):
        return jsonify({"error": "Quarter must be between 1 and 4"}), 400

    if not (2000 <= year <= datetime.datetime.now().year):
        return jsonify({"error": "Invalid year provided"}), 400

    service = FinancialExportService(DB_CONNECTION_STRING)
    filename = f"financial_export_Q{quarter}_{year}.csv"
    filepath = os.path.join(EXPORT_DIR, filename)

    try:
        logger.info(f"Initiating financial data export for Q{quarter} {year}")
        df = service.get_financial_data(quarter, year)

        if df.empty:
            logger.warning(f"No data found for Q{quarter} {year}")
            return jsonify({"message": f"No data found for Q{quarter} {year}"}), 200

        if not service.validate_data(df):
            logger.error(f"Data validation failed for Q{quarter} {year}")
            # Optionally, save invalid data or notify admins
            return jsonify({"error": "Data validation failed, export halted."}), 500

        if not service.export_to_csv(df, filepath):
            return jsonify({"error": "Failed to export data to CSV."}), 500

        logger.info(f"Successfully generated {filename}. Preparing for download.")
        return send_file(filepath, as_attachment=True, download_name=filename, mimetype='text/csv')

    except Exception as e:
        logger.error(f"An unexpected error occurred during export for Q{quarter} {year}: {e}", exc_info=True)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
