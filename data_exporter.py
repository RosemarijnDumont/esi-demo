# data_exporter.py

import pandas as pd

def export_data_to_excel(data: pd.DataFrame, filename: str):
    """
    Exports a pandas DataFrame to an Excel file with proper formatting for dates and currency.

    Args:
        data (pd.DataFrame): The DataFrame to export.
        filename (str): The name of the Excel file to create.
    """
    try:
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        # This allows for more control over cell formatting.
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')

        # Convert the DataFrame to an XlsxWriter Excel object.
        data.to_excel(writer, sheet_name='Report', index=False)

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = writer.book
        worksheet = writer.sheets['Report']

        # Define formats
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        currency_format = workbook.add_format({'num_format': '$#,##0.00'})

        # Apply formats to appropriate columns
        # Assuming column names are 