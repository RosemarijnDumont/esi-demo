import pandas as pd

def export_data_to_excel(data, filename):
    df = pd.DataFrame(data)

    # Apply date formatting
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

    # Apply currency formatting
    df['Amount'] = df['Amount'].apply(lambda x: f"${x:,.2f}")

    df.to_excel(filename, index=False)

    print(f"Data exported to {filename} with formatting applied.")

# Example usage:
if __name__ == "__main__":
    sample_data = {
        'Date': ['2023-01-01', '2023-01-15', '2023-02-01'],
        'Description': ['Item A', 'Item B', 'Item C'],
        'Amount': [100.50, 250.75, 1200.00]
    }
    export_data_to_excel(sample_data, 'analytics_report.xlsx')
