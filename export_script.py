import pandas as pd

def export_to_excel(dataframe, filename="report.xlsx"):
    """
    Exports a Pandas DataFrame to an Excel file.
    This function will be modified to include proper formatting.
    """
    # Placeholder for the actual export logic. 
    # The fix will involve configuring this to retain formatting.
    dataframe.to_excel(filename, index=False)
    print(f"Report exported to {filename}")

