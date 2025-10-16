
from locust import HttpUser, task, between
import os

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    host = os.getenv("TARGET_HOST", "http://localhost:8000")

    @task
    def bulk_import_small_file(self):
        csv_content = "name,email,role\nJohn Doe,john@example.com,user\nJane Smith,jane@example.com,admin"
        files = {"file": ("users.csv", csv_content, "text/csv")}
        self.client.post("/api/users/bulk-import", files=files)

    @task
    def bulk_import_large_file(self):
        num_users = 500 # Simulating a large file as per requirements
        csv_header = "name,email,role\n"
        csv_rows = [f"User {i},user{i}@example.com,user" for i in range(num_users)]
        csv_content = csv_header + "\n".join(csv_rows)
        files = {"file": ("large_users.csv", csv_content, "text/csv")}
        self.client.post("/api/users/bulk-import", files=files)

    @task
    def bulk_import_file_with_errors(self):
        csv_content = "name,email,role\nJohn Doe,john@example.com,user\nInvalid User,,invalid_role\nAnother User,another@example.com,admin"
        files = {"file": ("users_with_errors.csv", csv_content, "text/csv")}
        self.client.post("/api/users/bulk-import", files=files)
