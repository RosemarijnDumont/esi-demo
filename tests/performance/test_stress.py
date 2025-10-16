import pytest
from locust import HttpUser, task, between

class FinancialExportStressUser(HttpUser):
    wait_time = between(0.1, 0.5) # Shorter wait to simulate higher stress

    @task
    def export_data(self):
        self.client.get("/export")  # Assuming an endpoint for triggering export
