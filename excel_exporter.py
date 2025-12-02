# excel_exporter.py

import pandas as pd
import xlsxwriter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def export_data_to_excel(df: pd.DataFrame, output_path: str):
    """
    Exports a pandas DataFrame to an Excel file with specified formatting for date and currency columns.

    Args:
        df (pd.DataFrame): The DataFrame to export.
        output_path (str): The path to the output Excel file.
    """
    try:
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(output_path, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Report', index=False)

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = writer.book
        worksheet = writer.sheets['Report']

        # Define formats
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        currency_format = workbook.add_format({'num_format': '€#,##0.00'})  # Example for Euro

        # Apply formats to columns. This assumes you know the column names.
        # You might need to dynamically identify these columns based on your data.
        for col_idx, col_name in enumerate(df.columns):
            if 'date' in col_name.lower():  # Simple heuristic for date columns
                logging.info(f"Applying date format to column: {col_name}")
                worksheet.set_column(col_idx, col_idx, None, date_format)
            elif 'currency' in col_name.lower() or 'amount' in col_name.lower():  # Heuristic for currency/amount
                logging.info(f"Applying currency format to column: {col_name}")
                worksheet.set_column(col_idx, col_idx, None, currency_format)

        # Close the Pandas Excel writer and output the Excel file.
        writer.close()
        logging.info(f"Data successfully exported to {output_path} with formatting.")

    except Exception as e:
        logging.error(f"Error exporting data to Excel: {e}")
        raise

if __name__ == '__main__':
    # Example Usage:
    data = {
        'Date': pd.to_datetime(['2023-01-15', '2023-03-20', '2023-07-22']),
        'Revenue_Currency': [1234.56, 567.89, 9876.54],
        'Expenses_Amount': [123.45, 67.89, 987.65],
        'Description': ['Sale A', 'Sale B', 'Sale C']
    }
    df = pd.DataFrame(data)

    output_file = 'analytics_report_formatted.xlsx'
    export_data_to_excel(df, output_file)

    print(f"Please check '{output_file}' for the formatted report.")

