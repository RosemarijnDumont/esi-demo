
import pytest
import os
import pandas as pd
from datetime import datetime, timedelta
from src.financial_export_script import export_financial_data  # Assuming this is the script to be tested

OUTPUT_DIR = "./test_output"

@pytest.fixture(scope="module")
def setup_functional_test_data():
    """
    Generates a smaller, controlled dataset for functional testing.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("\nSetting up functional test data...")
    data = [
        {"transaction_id": "T001", "date": "2023-01-01", "amount": 100.50, "currency": "USD", "account_id": "ACC001", "description": "Sale A"},
        {"transaction_id": "T002", "date": "2023-01-05", "amount": 250.75, "currency": "EUR", "account_id": "ACC002", "description": "Service B"},
        {"transaction_id": "T003", "date": "2023-01-10", "amount": -50.00, "currency": "USD", "account_id": "ACC001", "description": "Refund C"},
        {"transaction_id": "T004", "date": "2023-02-15", "amount": 1234.56, "currency": "GBP", "account_id": "ACC003", "description": "Large Purchase D"},
        {"transaction_id": "T005", "date": "2023-02-20", "amount": 75.20, "currency": "USD", "account_id": "ACC002", "description": "Commission E"},
    ]
    df = pd.DataFrame(data)
    test_data_path = os.path.join(OUTPUT_DIR, "functional_test_data.csv")
    df.to_csv(test_data_path, index=False)
    print(f"Functional test data generated at: {test_data_path}")
    return test_data_path, df

def test_export_completeness_and_accuracy(setup_functional_test_data):
    """
    Tests if the export process generates a complete and accurate dataset.
    """
    input_file_path, expected_df = setup_functional_test_data
    output_file_name = os.path.join(OUTPUT_DIR, "functional_export_output.csv")

    print(f"\nStarting functional test (completeness and accuracy) with input: {input_file_path}...")
    try:
        export_financial_data(input_file_path, output_file_name)
    except Exception as e:
        pytest.fail(f"Financial export process failed during functional test: {e}")

    assert os.path.exists(output_file_name), "Exported file does not exist."
    exported_df = pd.read_csv(output_file_name)

    # 1. Check if the number of records matches
    assert len(exported_df) == len(expected_df), "Exported record count does not match input record count."

    # 2. Check for data integrity (e.g., all columns are present and data types are consistent)
    assert set(exported_df.columns) == set(expected_df.columns), "Exported columns do not match expected columns."
    # For more rigorous type checking, you'd iterate and compare dtypes or schema.

    # 3. Check for accuracy of data (e.g., specific values are correct)
    # Sort both dataframes to ensure direct comparison if order isn't guaranteed by export
    exported_df = exported_df.sort_values(by=list(exported_df.columns)).reset_index(drop=True)
    expected_df = expected_df.sort_values(by=list(expected_df.columns)).reset_index(drop=True)

    pd.testing.assert_frame_equal(exported_df, expected_df, check_dtype=True, check_exact=False, rtol=1e-05, atol=1e-08)
    print("Functional test: Data completeness and accuracy PASSED.")

def test_export_no_timeout_on_small_data(setup_functional_test_data):
    """
    Ensures the export process does not time out even with small, valid data.
    This is a basic check to ensure fundamental stability.
    """
    input_file_path, _ = setup_functional_test_data
    output_file_name = os.path.join(OUTPUT_DIR, "small_data_export_output.csv")
    TIMEOUT_SECONDS = 10 # A generous timeout for small data

    print(f"\nStarting timeout test on small data with input: {input_file_path}...")
    start_time = datetime.now()
    try:
        export_financial_data(input_file_path, output_file_name)
    except Exception as e:
        pytest.fail(f"Financial export process failed unexpectedly: {e}")
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    assert duration < TIMEOUT_SECONDS, f"Export timed out on small data. Took {duration:.2f}s, expected max {TIMEOUT_SECONDS}s"
    assert os.path.exists(output_file_name), "Exported file for small data test does not exist."
    print("Functional test: No timeout on small data PASSED.")


def test_export_empty_input_file():
    """
    Tests the behavior of the export process with an empty input file.
    It should handle this gracefully, potentially exporting an empty file or a header only.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    empty_input_path = os.path.join(OUTPUT_DIR, "empty_input.csv")
    output_file_name = os.path.join(OUTPUT_DIR, "empty_export_output.csv")
    pd.DataFrame(columns=["transaction_id", "date", "amount"]).to_csv(empty_input_path, index=False)

    print(f"\nStarting functional test with empty input file: {empty_input_path}...")
    try:
        export_financial_data(empty_input_path, output_file_name)
    except Exception as e:
        pytest.fail(f"Financial export process failed with empty input: {e}")

    assert os.path.exists(output_file_name), "Exported file for empty input does not exist."
    exported_df = pd.read_csv(output_file_name)
    assert exported_df.empty, "Exported file for empty input should be empty (or only headers)."
    print("Functional test: Empty input file handled gracefully PASSED.")

