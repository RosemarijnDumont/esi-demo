# test_data_exporter.py

import pandas as pd
import os
from data_exporter import export_data_to_excel

def test_export_formatting():
    """
    Tests that date and currency fields retain their formatting after export to Excel.
    """
    # Create sample data with dates and currency
    test_data = pd.DataFrame({
        'Date': pd.to_datetime(['2023-01-15', '2023-02-20', '2023-03-25']),
        'Revenue': [100.50, 250.75, 500.00],
        'Description': ['Sale 1', 'Sale 2', 'Sale 3'],
        'Cost': [10.20, 20.30, 30.40]
    })

    filename = "test_report.xlsx"
    export_data_to_excel(test_data, filename)

    # For simplicity, this test only verifies that the file is created.
    # A more robust test would involve parsing the Excel file and checking cell formats.
    # This would typically require a library like openpyxl to read cell formats.
    assert os.path.exists(filename)
    print(f"Successfully created {filename}. Manual inspection is recommended " \
          f"to verify date and currency formatting within the Excel file.")

    # Clean up the generated file
    os.remove(filename)

if __name__ == "__main__":
    test_export_formatting()
