import pytest
from financial_export.export_process import FinancialExportProcess

def test_data_accuracy_and_completeness():
    exporter = FinancialExportProcess()
    exported_data = exporter.run_export()
    # Assume a function `validate_exported_data` exists to compare with source
    assert exporter.validate_exported_data(exported_data)
