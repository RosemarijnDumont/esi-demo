import pytest
from locust import HttpUser, task, between

class FinancialExportUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def export_data(self):
        self.client.get("/export")  # Assuming an endpoint for triggering export
