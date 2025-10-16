
import pytest
from playwright.sync_api import Page, expect
from faker import Faker

faker = Faker()

BASE_URL = "http://localhost:8000"  # Assuming your frontend is served here and backend on 8000

def generate_csv_file(num_users, include_errors=False):
    header = "name,email,role\n"
    rows = []
    for i in range(num_users):
        name = faker.name()
        email = faker.email()
        role = faker.random_element(elements=("user", "admin"))
        rows.append(f"{name},{email},{role}")
    if include_errors:
        rows.append("Invalid User,,invalid_role") # Add a row with an error
    return header + "\n".join(rows)

def test_successful_bulk_import(page: Page):
    page.goto(f"{BASE_URL}/upload") # Assuming a dedicated upload page

    # Generate a valid CSV
    csv_content = generate_csv_file(3)
    with open("temp_users.csv", "w") as f:
        f.write(csv_content)

    # Upload the file
    page.set_input_files("input[type='file']", "temp_users.csv")
    page.click("button[type='submit']")

    # Assert success message and imported count
    expect(page.locator("data-testid=import-status")).to_contain_text("Bulk import completed")
    expect(page.locator("data-testid=imported-count")).to_contain_text("3 users imported")
    expect(page.locator("data-testid=error-list")).not_to_be_visible()

def test_bulk_import_with_errors(page: Page):
    page.goto(f"{BASE_URL}/upload")

    # Generate CSV with some errors
    csv_content = generate_csv_file(2, include_errors=True)
    with open("temp_users_with_errors.csv", "w") as f:
        f.write(csv_content)

    # Upload the file
    page.set_input_files("input[type='file']", "temp_users_with_errors.csv")
    page.click("button[type='submit']")

    # Assert partial success and error messages
    expect(page.locator("data-testid=import-status")).to_contain_text("Bulk import completed with errors")
    expect(page.locator("data-testid=imported-count")).to_contain_text("2 users imported")
    expect(page.locator("data-testid=error-list")).to_be_visible()
    expect(page.locator("data-testid=error-list")).to_contain_text("Invalid role")

def test_bulk_import_empty_file_frontend_validation(page: Page):
    page.goto(f"{BASE_URL}/upload")

    # Attempt to upload an empty file
    with open("empty.csv", "w") as f:
        f.write("")

    page.set_input_files("input[type='file']", "empty.csv")
    page.click("button[type='submit']")

    # Expect frontend validation error (or backend error displayed on frontend)
    expect(page.locator("data-testid=error-message")).to_contain_text("Uploaded CSV file is empty.")

def test_bulk_import_invalid_file_type_frontend_validation(page: Page):
    page.goto(f"{BASE_URL}/upload")

    # Attempt to upload an invalid file type
    with open("invalid.txt", "w") as f:
        f.write("not a csv")

    page.set_input_files("input[type='file']", "invalid.txt")
    page.click("button[type='submit']")

    # Expect frontend validation error (or backend error displayed on frontend)
    expect(page.locator("data-testid=error-message")).to_contain_text("Invalid file type")

def test_bulk_import_large_file_e2e_display(page: Page):
    page.goto(f"{BASE_URL}/upload")

    # Generate a large CSV without errors for a more realistic scenario
    csv_content = generate_csv_file(100) # Use a moderate size for E2E to avoid very long test runtimes
    with open("large_users_e2e.csv", "w") as f:
        f.write(csv_content)

    page.set_input_files("input[type='file']", "large_users_e2e.csv")
    page.click("button[type='submit']")

    # Assert success and imported count
    expect(page.locator("data-testid=import-status")).to_contain_text("Bulk import completed")
    expect(page.locator("data-testid=imported-count")).to_contain_text("100 users imported")
    expect(page.locator("data-testid=error-list")).not_to_be_visible()
