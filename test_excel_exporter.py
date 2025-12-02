# test_excel_exporter.py

import pandas as pd
import openpyxl
import os
import pytest
from excel_exporter import export_data_to_excel

# Fixture for a sample DataFrame
@pytest.fixture
def sample_dataframe():
    data = {
        'Order_Date': pd.to_datetime(['2023-01-01', '2023-02-15', '2023-03-30']),
        'Transaction_Currency': [100.50, 250.75, 50.00],
        'Amount': [10.20, 20.30, 30.40],
        'Product': ['A', 'B', 'C']
    }
    return pd.DataFrame(data)

# Test case for successful export and formatting
def test_export_data_to_excel_formatting(sample_dataframe, tmp_path):
    output_file = tmp_path / "test_report_formatted.xlsx"
    export_data_to_excel(sample_dataframe, output_file)

    assert os.path.exists(output_file)

    # Verify formatting using openpyxl
    workbook = openpyxl.load_workbook(output_file)
    sheet = workbook.active

    # Check date formatting (Column A: Order_Date)
    # The format code might vary slightly depending on openpyxl's interpretation
    assert sheet['A2'].number_format == 'dd/mm/yyyy'
    assert sheet['A3'].number_format == 'dd/mm/yyyy'

    # Check currency formatting (Column B: Transaction_Currency)
    assert sheet['B2'].number_format == '€#,##0.00'
    assert sheet['B3'].number_format == '€#,##0.00' 

    # Check for another currency/amount column (Column C: Amount)
    assert sheet['C2'].number_format == '€#,##0.00'

    workbook.close()

# Test case for error handling (e.g., invalid path)
def test_export_data_to_excel_error_handling(sample_dataframe):
    invalid_path = "/nonexistent_dir/report.xlsx"
    with pytest.raises(Exception):
        export_data_to_excel(sample_dataframe, invalid_path)


