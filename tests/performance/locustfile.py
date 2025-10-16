
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def login_and_dashboard(self):
        self.client.post("/login", {"username": "testuser", "password": "password123"})
        self.client.get("/dashboard")

    @task
    def reports_page(self):
        self.client.post("/login", {"username": "testuser", "password": "password123"})
        self.client.get("/reports")
