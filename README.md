# esi-demo
adapt and test

## Analytics Report Export Formatting Fix

This update addresses a bug where exported Excel reports were losing their date and currency formatting. The `excel_exporter.py` script has been updated to explicitly apply formatting using `xlsxwriter` during the export process. 

### Changes Implemented:
- **`excel_exporter.py`**: Modified to include logic for identifying date and currency columns (based on column name heuristics) and applying `dd/mm/yyyy` and `€#,##0.00` formats respectively. 
- **Logging**: Added logging to the export process to assist with debugging and track formatting application.

### How to Use:
To export data with proper formatting, simply use the `export_data_to_excel` function from `excel_exporter.py`:

```python
import pandas as pd
from excel_exporter import export_data_to_excel

# Your DataFrame
data = {
    'Date': pd.to_datetime(['2023-01-15', '2023-03-20', '2023-07-22']),
    'Revenue_Currency': [1234.56, 567.89, 9876.54],
    'Expenses_Amount': [123.45, 67.89, 987.65],
    'Description': ['Sale A', 'Sale B', 'Sale C']
}
df = pd.DataFrame(data)

output_file = 'my_analytics_report.xlsx'
export_data_to_excel(df, output_file)
```

### Future Improvements:
- **Dynamic Column Identification**: Enhance the column identification logic to be more robust (e.g., based on data types or a configuration).
- **Locale-Specific Formatting**: Implement broader support for different currency symbols and date formats based on user locale settings.
- **Excel Template Integration**: If a pre-defined Excel template is preferred, the script could be adapted to load a template and apply formatting to specific cells/ranges within it.
