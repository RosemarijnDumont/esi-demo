# src/data_aggregation_service.py

import time
import logging
from typing import Dict, Any, List
from src.cache_strategy import CacheManager, InMemoryCache

logger = logging.getLogger(__name__)

# Initialize the cache manager for the aggregation service
# In a real application, this might be configured via dependency injection or a global config
cache_manager = CacheManager(InMemoryCache(default_ttl=300)) # Default 5 min TTL for aggregation

class DataAggregationService:
    """Service responsible for aggregating raw data into dashboard-ready formats."""

    def __init__(self):
        logger.info("DataAggregationService initialized.")

    @cache_manager.cache(ttl=300, key_prefix="dashboard_summary_")
    def get_dashboard_summary(self, user_id: int, period: str = "daily") -> Dict[str, Any]:
        """Aggregates and returns high-level summary data for the dashboard."""
        logger.info(f"[NON-CACHED] Aggregating summary data for user_id: {user_id}, period: {period}")
        # Simulate complex database queries and aggregations
        time.sleep(1.5) 
        data = {
            "total_sales": 125000.50,
            "new_customers": 150,
            "conversion_rate": 0.035,
            "period": period,
            "user_id": user_id,
            "timestamp": time.time()
        }
        logger.debug(f"Generated summary data: {data}")
        return data

    @cache_manager.cache(ttl=600, key_prefix="dashboard_trends_")
    def get_sales_trends(self, user_id: int, product_category: str) -> List[Dict[str, Any]]:
        """Aggregates and returns sales trend data over time for a given category."""
        logger.info(f"[NON-CACHED] Aggregating sales trends for user_id: {user_id}, category: {product_category}")
        # Simulate a more intensive query
        time.sleep(2.0) 
        trends = [
            {"date": "2023-01-01", "sales": 1000},
            {"date": "2023-01-02", "sales": 1200},
            {"date": "2023-01-03", "sales": 1150},
            {"date": "2023-01-04", "sales": 1300},
        ]
        logger.debug(f"Generated sales trends: {trends}")
        return trends

    @cache_manager.cache(ttl=180, key_prefix="dashboard_top_products_")
    def get_top_performing_products(self, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Aggregates and returns a list of top-performing products."""
        logger.info(f"[NON-CACHED] Aggregating top products for user_id: {user_id}, limit: {limit}")
        time.sleep(1.0)
        products = [
            {"id": 101, "name": "Product A", "revenue": 5000},
            {"id": 102, "name": "Product B", "revenue": 4500},
            {"id": 103, "name": "Product C", "revenue": 3800},
        ]
        logger.debug(f"Generated top products: {products}")
        return products

    def refresh_dashboard_summary_cache(self, user_id: int, period: str = "daily") -> None:
        """Manually invalidates the cache for dashboard summary data."""
        key = cache_manager.cache(key_prefix="dashboard_summary_").__wrapped__.__name__ # This is a bit hacky, relies on decorator internal
        # A more robust solution would be to generate the key deterministically here
        args_key = "-".join(map(str, [user_id, period]))
        kwargs_key = ""
        full_key = f"dashboard_summary_get_dashboard_summary__{args_key}__{kwargs_key}"

        cache_manager.strategy.invalidate(full_key)
        logger.info(f"Manually invalidated cache for dashboard summary for user_id: {user_id}, period: {period}")

# Example usage (for demonstration/testing)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)

    service = DataAggregationService()

    user_id_1 = 123
    user_id_2 = 456

    # --- Test Dashboard Summary ---
    print("\n--- First call to get_dashboard_summary (user_id_1) ---")
    start_time = time.time()
    summary1_1 = service.get_dashboard_summary(user_id_1, "daily")
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f}s, Summary: {summary1_1}")

    print("\n--- Second call to get_dashboard_summary (user_id_1) (should be cached) ---")
    start_time = time.time()
    summary1_2 = service.get_dashboard_summary(user_id_1, "daily")
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f}s, Summary: {summary1_2}")
    assert summary1_1 == summary1_2

    print("\n--- First call to get_dashboard_summary (user_id_2) ---")
    start_time = time.time()
    summary2_1 = service.get_dashboard_summary(user_id_2, "monthly")
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f}s, Summary: {summary2_1}")

    # --- Test Sales Trends ---
    print("\n--- First call to get_sales_trends ---")
    start_time = time.time()
    trends1_1 = service.get_sales_trends(user_id_1, "Electronics")
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f}s, Trends: {trends1_1}")

    print("\n--- Second call to get_sales_trends (should be cached) ---")
    start_time = time.time()
    trends1_2 = service.get_sales_trends(user_id_1, "Electronics")
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f}s, Trends: {trends1_2}")
    assert trends1_1 == trends1_2

    # --- Test Manual Invalidation ---
    print("\n--- Manually invalidating cache for user_id_1 daily summary ---")
    service.refresh_dashboard_summary_cache(user_id_1, "daily")

    print("\n--- Call to get_dashboard_summary (user_id_1) after manual invalidation (should re-compute) ---")
    start_time = time.time()
    summary1_3 = service.get_dashboard_summary(user_id_1, "daily")
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f}s, Summary: {summary1_3}")
    assert summary1_1 != summary1_3 # Due to timestamp in data

    # Simulate cache expiry
    print("\n--- Waiting for dashboard summary cache to expire (6 seconds) ---")
    time.sleep(6) # summary cache has 5s TTL + 1s buffer

    print("\n--- Call to get_dashboard_summary (user_id_1) after TTL expiry (should re-compute) ---")
    start_time = time.time()
    summary1_4 = service.get_dashboard_summary(user_id_1, "daily")
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f}s, Summary: {summary1_4}")
    assert summary1_3 != summary1_4

    print("\n--- Clearing all caches via CacheManager ---")
    cache_manager.strategy.clear()
    start_time = time.time()
    summary1_5 = service.get_dashboard_summary(user_id_1, "daily")
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f}s, Summary: {summary1_5}")
