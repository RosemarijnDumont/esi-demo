# test/test_caching.py

import unittest
import time
import logging
from src.cache_strategy import InMemoryCache, CacheManager
from src.data_aggregation_service import DataAggregationService, cache_manager as service_cache_manager
from src.dashboard_api import DashboardAPI

# Configure logging for tests to suppress INFO/DEBUG from modules, only show errors
logging.basicConfig(level=logging.CRITICAL)

class TestInMemoryCache(unittest.TestCase):

    def setUp(self):
        self.cache = InMemoryCache(default_ttl=1)
        self.cache.clear() # Ensure cache is clean before each test

    def test_set_and_get(self):
        self.cache.set("key1", "value1")
        self.assertEqual(self.cache.get("key1"), "value1")

    def test_get_non_existent_key(self):
        self.assertIsNone(self.cache.get("non_existent_key"))

    def test_ttl_expiry(self):
        self.cache.set("key_ttl", "value_ttl", ttl=1)
        self.assertEqual(self.cache.get("key_ttl"), "value_ttl")
        time.sleep(1.1)  # Wait for TTL to expire
        self.assertIsNone(self.cache.get("key_ttl"))

    def test_invalidate(self):
        self.cache.set("key_to_invalidate", "old_value")
        self.assertEqual(self.cache.get("key_to_invalidate"), "old_value")
        self.cache.invalidate("key_to_invalidate")
        self.assertIsNone(self.cache.get("key_to_invalidate"))

    def test_clear(self):
        self.cache.set("keyA", "valueA")
        self.cache.set("keyB", "valueB")
        self.assertIsNotNone(self.cache.get("keyA"))
        self.cache.clear()
        self.assertIsNone(self.cache.get("keyA"))
        self.assertIsNone(self.cache.get("keyB"))

    def test_set_with_zero_ttl_no_expiry(self):
        self.cache.set("key_no_ttl", "value_no_ttl", ttl=0) # ttl=0 means no expiry
        time.sleep(0.5)
        self.assertIsNotNone(self.cache.get("key_no_ttl"))
        time.sleep(1.0) # Wait past default TTL of 1s (but this key has 0 TTL)
        self.assertIsNotNone(self.cache.get("key_no_ttl"))


class TestCacheManager(unittest.TestCase):

    def setUp(self):
        self.cache_manager = CacheManager(InMemoryCache(default_ttl=1))
        self.cache_manager.strategy.clear()

    def test_decorator_caches_result(self):
        call_count = [0]

        @self.cache_manager.cache(ttl=1)
        def test_func():
            call_count[0] += 1
            return "result"
        
        # First call, should execute function
        result1 = test_func()
        self.assertEqual(result1, "result")
        self.assertEqual(call_count[0], 1)

        # Second call, within TTL, should be cached
        result2 = test_func()
        self.assertEqual(result2, "result")
        self.assertEqual(call_count[0], 1) # Should not have incremented

        # Wait for TTL to expire
        time.sleep(1.1)

        # Third call, after TTL, should execute function again
        result3 = test_func()
        self.assertEqual(result3, "result")
        self.assertEqual(call_count[0], 2) # Should have incremented again

    def test_decorator_with_different_args(self):
        call_count = [0]

        @self.cache_manager.cache()
        def test_func_args(a, b):
            call_count[0] += 1
            return f"{a}-{b}"
        
        test_func_args(1, 2)
        self.assertEqual(call_count[0], 1)
        test_func_args(1, 2) # Same args, cached
        self.assertEqual(call_count[0], 1)
        test_func_args(3, 4) # Different args, new computation
        self.assertEqual(call_count[0], 2)
        test_func_args(1, 2) # Back to original, still cached
        self.assertEqual(call_count[0], 2)

    def test_key_prefix(self):
        @self.cache_manager.cache(key_prefix="my_prefix_")
        def another_func():
            return "data"
        
        another_func()
        # Directly check if a key with the prefix exists in the cache strategy
        # This is a bit of an implementation detail exposure for testing purposes
        found = False
        for key in self.cache_manager.strategy._cache.keys():
            if key.startswith("my_prefix_another_func__"):
                found = True
                break
        self.assertTrue(found, "Cache key with prefix was not found")

    def test_change_cache_strategy(self):
        initial_strategy = self.cache_manager.strategy
        new_strategy = InMemoryCache(default_ttl=60)
        self.cache_manager.strategy = new_strategy
        self.assertIs(self.cache_manager.strategy, new_strategy)
        self.assertIsNot(self.cache_manager.strategy, initial_strategy)

    def test_change_cache_strategy_invalid_type(self):
        with self.assertRaises(TypeError):
            self.cache_manager.strategy = "not a strategy"


class TestDataAggregationService(unittest.TestCase):

    def setUp(self):
        # Ensure the shared cache manager for the service is clean before each test
        service_cache_manager.strategy.clear()
        self.service = DataAggregationService()
        self.user_id = 999
        self.period = "test_daily"

    def test_get_dashboard_summary_caches(self):
        start_time = time.time()
        summary1 = self.service.get_dashboard_summary(self.user_id, self.period)
        duration1 = time.time() - start_time
        self.assertGreater(duration1, 1.0) # Should take significant time initially

        start_time = time.time()
        summary2 = self.service.get_dashboard_summary(self.user_id, self.period)
        duration2 = time.time() - start_time
        self.assertLess(duration2, 0.1) # Should be fast due to cache
        self.assertEqual(summary1, summary2)

    def test_refresh_dashboard_summary_cache_invalidates(self):
        summary_initial = self.service.get_dashboard_summary(self.user_id, self.period)
        
        # Invalidate specific entry
        self.service.refresh_dashboard_summary_cache(self.user_id, self.period)

        start_time = time.time()
        summary_after_refresh = self.service.get_dashboard_summary(self.user_id, self.period)
        duration_after_refresh = time.time() - start_time
        self.assertGreater(duration_after_refresh, 1.0) # Should re-compute
        self.assertNotEqual(summary_initial['timestamp'], summary_after_refresh['timestamp']) # Ensure new data was generated

    def test_different_args_not_cached_together(self):
        summary_user1_daily = self.service.get_dashboard_summary(1, "daily")
        summary_user2_daily = self.service.get_dashboard_summary(2, "daily")
        summary_user1_monthly = self.service.get_dashboard_summary(1, "monthly")

        # Call again, should be cached
        _ = self.service.get_dashboard_summary(1, "daily")

        # Ensure different calls are distinct in cache by checking for re-computation time
        start_time = time.time()
        # This call should be cached
        _ = self.service.get_dashboard_summary(1, "daily")
        duration = time.time() - start_time
        self.assertLess(duration, 0.1)

        start_time = time.time()
        # This call was for a different user, should be cached IF it was called before
        _ = self.service.get_dashboard_summary(2, "daily")
        duration = time.time() - start_time
        self.assertLess(duration, 0.1)


class TestDashboardAPI(unittest.TestCase):

    def setUp(self):
        service_cache_manager.strategy.clear() # Clear cache before each API test
        self.api = DashboardAPI()
        self.user_id = 789

    def test_full_dashboard_data_loading_times(self):
        # First call should take longer due to cache misses
        start_time = time.time()
        data1 = self.api.get_full_dashboard_data(self.user_id, "daily")
        duration1 = time.time() - start_time
        # Assuming total aggregation time (1.5 + 2.0 + 1.0) = 4.5 seconds approximately
        self.assertGreater(duration1, 4.0)

        # Second call should be significantly faster due to cache hits
        start_time = time.time()
        data2 = self.api.get_full_dashboard_data(self.user_id, "daily")
        duration2 = time.time() - start_time
        self.assertLess(duration2, 0.1) # Should be very fast

        # Assert data consistency (timestamps within the aggregated data will differ if re-computed)
        self.assertEqual(data1['summary']['timestamp'], data2['summary']['timestamp'])
        self.assertEqual(data1['sales_trends'], data2['sales_trends'])
        self.assertEqual(data1['top_products'], data2['top_products'])

    def test_dashboard_data_after_partial_invalidation(self):
        data_initial = self.api.get_full_dashboard_data(self.user_id, "daily")
        time.sleep(0.05) # Small sleep to ensure timestamps differ if recomputed
        self.api.aggregation_service.refresh_dashboard_summary_cache(self.user_id, "daily")

        start_time = time.time()
        data_after_invalidation = self.api.get_full_dashboard_data(self.user_id, "daily")
        duration_after_invalidation = time.time() - start_time

        # Summary data should be re-computed (slow path for summary)
        self.assertGreater(duration_after_invalidation, 1.0)
        self.assertNotEqual(data_initial['summary']['timestamp'], data_after_invalidation['summary']['timestamp'])

        # Other data should still be cached (fast path for trends and products)
        self.assertEqual(data_initial['sales_trends'], data_after_invalidation['sales_trends'])
        self.assertEqual(data_initial['top_products'], data_after_invalidation['top_products'])

    def test_dashboard_load_with_different_user(self):
        # Load for user A
        _ = self.api.get_full_dashboard_data(self.user_id, "daily")
        
        # Load for user B, should hit cache misses for new user
        start_time = time.time()
        data_user_b = self.api.get_full_dashboard_data(self.user_id + 1, "daily")
        duration_user_b = time.time() - start_time
        self.assertGreater(duration_user_b, 4.0)


if __name__ == '__main__':
    unittest.main()
