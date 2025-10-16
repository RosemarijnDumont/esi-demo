
import csv
from io import StringIO

def parse_csv_data(csv_content: str) -> list[dict]:
    required_columns = ["name", "email", "role"]
    users = []
    f = StringIO(csv_content)
    reader = csv.reader(f)

    try:
        header = next(reader)
    except StopIteration:
        raise ValueError("Uploaded CSV file is empty.")

    # Validate required columns
    for col in required_columns:
        if col not in header:
            raise ValueError(f"Missing required column: {col}")

    for i, row in enumerate(reader):
        if not row:  # Skip empty rows
            continue

        if len(row) != len(header):
            raise ValueError(f"CSV row {i+2} has incorrect number of columns. Expected {len(header)}, got {len(row)}.")

        user_data = dict(zip(header, row))
        users.append({
            "name": user_data.get("name", ""),
            "email": user_data.get("email", ""),
            "role": user_data.get("role", ""),
        })
    return users
