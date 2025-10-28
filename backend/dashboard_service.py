
import time
from functools import lru_cache

import redis

# Assuming a database connection object 'db' is available globally or passed in
from .database import db

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class DashboardService:
    def get_dashboard_data(self, user_id):
        start_time = time.time()
        # 1. Optimized database queries
        # Example: Fetching user-specific data, ensure 'user_id' is indexed
        user_data = self._get_user_summary_data(user_id)
        
        # Example: Fetching recent activities, ensure 'timestamp' is indexed
        recent_activities = self._get_recent_activities(user_id, limit=10)

        # Example: Fetching aggregated reports data, ensure appropriate indexes
        reports_summary = self._get_reports_summary(user_id)

        end_time = time.time()
        print(f"Dashboard data retrieval time: {end_time - start_time:.4f} seconds")

        return {
            "user_data": user_data,
            "recent_activities": recent_activities,
            "reports_summary": reports_summary,
        }

    @lru_cache(maxsize=128)  # Simple in-memory cache for frequently accessed static data
    def _get_user_summary_data(self, user_id):
        # Simulate a database call with a delay
        time.sleep(0.05) 
        # In a real application, this would be a query like:
        # return db.execute("SELECT * FROM user_summary WHERE user_id = %s", (user_id,)).fetchone()
        return {"user_id": user_id, "total_projects": 5, "completed_tasks": 25}

    @lru_cache(maxsize=64)  # Cache recent activities for a short period if they don't change often
    def _get_recent_activities(self, user_id, limit):
        # Simulate a database call with a delay
        # Check Redis cache first
        cache_key = f"recent_activities:{user_id}:{limit}"
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return eval(cached_data.decode('utf-8')) # In a real app, use JSON serialization

        time.sleep(0.1)
        # In a real application, this would be a query like:
        # return db.execute("SELECT * FROM activities WHERE user_id = %s ORDER BY timestamp DESC LIMIT %s", (user_id, limit,)).fetchall()
        activities = [
            {"id": 1, "description": "Task A completed", "timestamp": "2023-10-26T10:00:00Z"},
            {"id": 2, "description": "New project created", "timestamp": "2023-10-26T09:30:00Z"},
        ]
        # Store in Redis cache for 60 seconds
        redis_client.setex(cache_key, 60, str(activities))
        return activities

    def _get_reports_summary(self, user_id):
        # Simulate a more complex database call with aggregation
        # Check Redis cache first
        cache_key = f"reports_summary:{user_id}"
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return eval(cached_data.decode('utf-8'))

        time.sleep(0.2)
        # In a real application, this would involve aggregated queries like:
        # return db.execute("SELECT COUNT(*), AVG(duration) FROM reports WHERE user_id = %s", (user_id,)).fetchone()
        summary = {"total_reports": 10, "average_score": 85.5}
        # Store in Redis cache for 300 seconds (5 minutes)
        redis_client.setex(cache_key, 300, str(summary))
        return summary

class ReportsService:
    def get_reports_overview(self, user_id, page=1, page_size=20):
        start_time = time.time()
        # Optimized database queries for reports overview
        # Example: Fetching paginated reports, ensure 'user_id' and 'timestamp' are indexed
        reports = self._fetch_paginated_reports(user_id, page, page_size)
        total_reports = self._get_total_reports_count(user_id)

        end_time = time.time()
        print(f"Reports overview retrieval time: {end_time - start_time:.4f} seconds")

        return {
            "reports": reports,
            "total_reports": total_reports,
            "page": page,
            "page_size": page_size,
        }

    def _fetch_paginated_reports(self, user_id, page, page_size):
        cache_key = f"paginated_reports:{user_id}:{page}:{page_size}"
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return eval(cached_data.decode('utf-8'))

        time.sleep(0.15)
        # In a real application:
        # offset = (page - 1) * page_size
        # return db.execute("SELECT * FROM reports WHERE user_id = %s ORDER BY created_at DESC LIMIT %s OFFSET %s", 
        #                   (user_id, page_size, offset)).fetchall()
        reports = [
            {"id": 101, "title": "Monthly Performance", "date": "2023-09-30"},
            {"id": 102, "title": "Quarterly Review", "date": "2023-08-15"},
        ]
        redis_client.setex(cache_key, 120, str(reports))
        return reports

    def _get_total_reports_count(self, user_id):
        cache_key = f"total_reports_count:{user_id}"
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return int(cached_data.decode('utf-8'))

        time.sleep(0.05)
        # In a real application:
        # return db.execute("SELECT COUNT(*) FROM reports WHERE user_id = %s", (user_id,)).fetchone()[0]
        count = 15
        redis_client.setex(cache_key, 3600, str(count))
        return count
