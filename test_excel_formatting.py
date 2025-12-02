# test_excel_formatting.py
import pytest
import pandas as pd
from datetime import datetime

# Mock function to simulate the existing export logic without the fix
def export_report_to_excel_old(data: dict, file_path: str):
    df = pd.DataFrame(data)
    for col in ['Date', 'TransactionDate']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    df.to_excel(file_path, index=False)

# Mock function to simulate the *new* export logic with the fix
def export_report_to_excel_new(data: dict, file_path: str):
    df = pd.DataFrame(data)
    for col in ['Date', 'TransactionDate']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col]).dt.strftime('%m/%d/%Y') # Enforce MM/DD/YYYY
    for col in ['Amount', 'Price']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f'${x:,.2f}') # Enforce currency format
    df.to_excel(file_path, index=False)

@pytest.fixture
def sample_data_date_currency():
    return {
        'Date': ['2023-01-15', '2023-02-20'],
        'Amount': [1234.56, 789.00],
        'Description': ['Item A', 'Item B']
    }

@pytest.fixture
def sample_data_various_formats():
    return {
        'TransactionDate': ['2022-11-01', '2023-03-25'],
        'Price': [99.99, 1500.25],
        'Quantity': [2, 1]
    }

def test_date_formatting_old_issue(sample_data_date_currency, tmp_path):
    # This test demonstrates the *original* bug where formatting is lost
    file_path = tmp_path / "report_old_date.xlsx"
    export_report_to_excel_old(sample_data_date_currency, file_path)

    df_exported = pd.read_excel(file_path)
    # Pandas often infers datetime, but display format might be generic
    # We're specifically looking for the fix to apply the string format before export
    assert isinstance(df_exported['Date'].iloc[0], datetime) # Expect datetime object if not explicitly formatted

def test_currency_formatting_old_issue(sample_data_date_currency, tmp_path):
    # This test demonstrates the *original* bug where formatting is lost
    file_path = tmp_path / "report_old_currency.xlsx"
    export_report_to_excel_old(sample_data_date_currency, file_path)

    df_exported = pd.read_excel(file_path)
    assert isinstance(df_exported['Amount'].iloc[0], (float, int)) # Expect numeric if not explicitly formatted

def test_date_formatting_new_fix(sample_data_date_currency, tmp_path):
    # Test to ensure date fields retain MM/DD/YYYY formatting with the fix
    file_path = tmp_path / "report_new_date.xlsx"
    export_report_to_excel_new(sample_data_date_currency, file_path)

    df_exported = pd.read_excel(file_path)
    # When formatted as string 'MM/DD/YYYY', pandas will read it as string
    assert df_exported['Date'].iloc[0] == '01/15/2023'
    assert df_exported['Date'].iloc[1] == '02/20/2023'
    assert isinstance(df_exported['Date'].iloc[0], str)

def test_currency_formatting_new_fix(sample_data_date_currency, tmp_path):
    # Test to ensure currency fields retain $X,XXX.XX formatting with the fix
    file_path = tmp_path / "report_new_currency.xlsx"
    export_report_to_excel_new(sample_data_date_currency, file_path)

    df_exported = pd.read_excel(file_path)
    # When formatted as string '$X,XXX.XX', pandas will read it as string
    assert df_exported['Amount'].iloc[0] == '$1,234.56'
    assert df_exported['Amount'].iloc[1] == '$789.00'
    assert isinstance(df_exported['Amount'].iloc[0], str)

def test_multiple_date_currency_fields_new_fix(sample_data_various_formats, tmp_path):
    # Test with multiple date and currency fields to ensure consistency
    file_path = tmp_path / "report_new_multiple.xlsx"
    export_report_to_excel_new(sample_data_various_formats, file_path)

    df_exported = pd.read_excel(file_path)
    assert df_exported['TransactionDate'].iloc[0] == '11/01/2022'
    assert df_exported['TransactionDate'].iloc[1] == '03/25/2023'
    assert isinstance(df_exported['TransactionDate'].iloc[0], str)

    assert df_exported['Price'].iloc[0] == '$99.99'
    assert df_exported['Price'].iloc[1] == '$1,500.25'
    assert isinstance(df_exported['Price'].iloc[0], str)

def test_regression_other_fields_unaffected(sample_data_various_formats, tmp_path):
    # Ensure other non-formatted fields are not negatively impacted
    file_path = tmp_path / "report_new_regression.xlsx"
    export_report_to_excel_new(sample_data_various_formats, file_path)

    df_exported = pd.read_excel(file_path)
    assert df_exported['Quantity'].iloc[0] == 2
    assert df_exported['Quantity'].iloc[1] == 1
    assert isinstance(df_exported['Quantity'].iloc[0], int)
