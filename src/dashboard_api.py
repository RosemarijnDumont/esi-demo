# src/dashboard_api.py

import logging
import time
from typing import Dict, Any
from src.data_aggregation_service import DataAggregationService

logger = logging.getLogger(__name__)

class DashboardAPI:
    """Simulates the API endpoint that serves dashboard data requests."""

    def __init__(self):
        self.aggregation_service = DataAggregationService()
        logger.info("DashboardAPI initialized, using DataAggregationService.")

    def get_full_dashboard_data(self, user_id: int, period: str = "daily") -> Dict[str, Any]:
        """Assembles all necessary data for the dashboard view."""
        start_time = time.time()
        logger.info(f"Fetching full dashboard data for user_id: {user_id}, period: {period}")

        # These calls will leverage the caching implemented in DataAggregationService
        summary = self.aggregation_service.get_dashboard_summary(user_id, period)
        sales_trends = self.aggregation_service.get_sales_trends(user_id, "All")
        top_products = self.aggregation_service.get_top_performing_products(user_id, 5)

        dashboard_data = {
            "summary": summary,
            "sales_trends": sales_trends,
            "top_products": top_products,
            "generation_time": time.time()
        }
        end_time = time.time()
        load_time = end_time - start_time
        logger.info(f"Dashboard data for user_id {user_id} loaded in {load_time:.4f} seconds.")
        return dashboard_data

# Example usage (for demonstration/testing)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)

    api = DashboardAPI()

    user_id = 123

    print("\n--- First dashboard load (should trigger aggregations) ---")
    dashboard_data_1 = api.get_full_dashboard_data(user_id, "daily")
    # print(f"Dashboard Data 1: {dashboard_data_1}")

    print("\n--- Second dashboard load (should use cached data) ---")
    dashboard_data_2 = api.get_full_dashboard_data(user_id, "daily")
    # print(f"Dashboard Data 2: {dashboard_data_2}")
    # Verifying that timestamps indicate cached data
    assert dashboard_data_1['summary']['timestamp'] == dashboard_data_2['summary']['timestamp']
    assert dashboard_data_1['sales_trends'] == dashboard_data_2['sales_trends']
    assert dashboard_data_1['top_products'] == dashboard_data_2['top_products']

    print("\n--- Third dashboard load for a different user (should trigger new aggregations) ---")
    dashboard_data_3 = api.get_full_dashboard_data(456, "daily")
    # print(f"Dashboard Data 3: {dashboard_data_3}")

    print("\n--- Demonstrating cache invalidation for a specific part of the dashboard ---")
    service = api.aggregation_service
    service.refresh_dashboard_summary_cache(user_id, "daily")

    print("\n--- Dashboard load after summary cache invalidation (summary re-aggregated, others cached) ---")
    dashboard_data_4 = api.get_full_dashboard_data(user_id, "daily")
    assert dashboard_data_1['summary']['timestamp'] != dashboard_data_4['summary']['timestamp'] # Summary should be new
    assert dashboard_data_1['sales_trends'] == dashboard_data_4['sales_trends'] # Others should still be cached

    print("\n--- Waiting for some caches to expire ---")
    print("Waiting 6 seconds...")
    time.sleep(6) # Summary cache TTL is 5s, so it should expire
                   # Sales trends TTL is 10 min, Top products TTL is 3 min, so they should remain cached

    print("\n--- Dashboard load after summary cache expiry (summary re-aggregated, others still cached) ---")
    dashboard_data_5 = api.get_full_dashboard_data(user_id, "daily")
    assert dashboard_data_4['summary']['timestamp'] != dashboard_data_5['summary']['timestamp'] # Summary should be new
    assert dashboard_data_4['sales_trends'] == dashboard_data_5['sales_trends']

    print("\n--- Clearing entire cache and reloading ---")
    service.cache_manager.strategy.clear()
    dashboard_data_6 = api.get_full_dashboard_data(user_id, "daily")
    assert dashboard_data_5['summary']['timestamp'] != dashboard_data_6['summary']['timestamp']
    assert dashboard_data_5['sales_trends'] != dashboard_data_6['sales_trends']
