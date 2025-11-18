import pandas as pd
from export_script import export_data_to_excel
import os

def test_excel_export_formatting():
    sample_data = {
        'Date': ['2023-01-01', '2023-01-15', '2023-02-01'],
        'Description': ['Item A', 'Item B', 'Item C'],
        'Amount': [100.50, 250.75, 1200.00]
    }
    test_filename = 'test_analytics_report.xlsx'

    export_data_to_excel(sample_data, test_filename)

    # Verify the file is created
    assert os.path.exists(test_filename)

    # Read the exported Excel file and check formatting
    df_exported = pd.read_excel(test_filename)

    # Check date formatting
    # The date is stored as a string in the Excel after strftime, so we check the string format directly
    assert df_exported['Date'][0] == '2023-01-01'
    assert df_exported['Date'][1] == '2023-01-15'

    # Check currency formatting
    assert df_exported['Amount'][0] == '$100.50'
    assert df_exported['Amount'][1] == '$250.75'
    assert df_exported['Amount'][2] == '$1,200.00'

    # Clean up the test file
    os.remove(test_filename)

    print("All export formatting tests passed!")

if __name__ == "__main__":
    test_excel_export_formatting()
