import pandas as pd

def generate_test_data():
    """
    Generates a Pandas DataFrame with various date and currency formats for testing.
    """
    data = {
        'Date_MM/DD/YYYY': pd.to_datetime(['01/15/2023', '02/29/2024', '12/01/2023'], format='%m/%d/%Y'),
        'Date_DD-MMM-YY': pd.to_datetime(['15-Jan-23', '29-Feb-24', '01-Dec-23'], format='%d-%b-%y'),
        'Currency_USD': [1234.56, 789.00, 12345.78],
        'Currency_EUR': [123.45, 678.90, 1234.56]
    }
    df = pd.DataFrame(data)
    
    # Convert currency columns to appropriate types for display
    df['Currency_USD'] = df['Currency_USD'].apply(lambda x: f'${x:,.2f}')
    df['Currency_EUR'] = df['Currency_EUR'].apply(lambda x: f'€{x:,.2f}')

    return df

