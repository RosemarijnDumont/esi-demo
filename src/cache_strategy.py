# src/cache_strategy.py

from abc import ABC, abstractmethod
import functools
import time
import logging
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)

class CacheStrategy(ABC):
    """Abstract base class for caching strategies."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Retrieves an item from the cache."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Sets an item in the cache."""
        pass

    @abstractmethod
    def invalidate(self, key: str) -> None:
        """Invalidates (removes) an item from the cache."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clears the entire cache."""
        pass


class InMemoryCache(CacheStrategy):
    """An in-memory caching strategy with a time-to-live (TTL)."""

    def __init__(self, default_ttl: int = 300):  # Default TTL of 5 minutes
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._default_ttl = default_ttl
        logger.info(f"Initialized InMemoryCache with default_ttl={self._default_ttl}s")

    def get(self, key: str) -> Optional[Any]:
        item = self._cache.get(key)
        if item and (item.get("expiry") is None or item["expiry"] > time.time()):
            logger.debug(f"Cache hit for key: {key}")
            return item["value"]
        elif item:
            logger.debug(f"Cache miss (expired) for key: {key}")
            self.invalidate(key)  # Remove expired item
        else:
            logger.debug(f"Cache miss for key: {key}")
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        actual_ttl = ttl if ttl is not None else self._default_ttl
        expiry = time.time() + actual_ttl if actual_ttl > 0 else None
        self._cache[key] = {"value": value, "expiry": expiry}
        logger.debug(f"Cache set for key: {key} with TTL: {actual_ttl}s")

    def invalidate(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]
            logger.info(f"Cache invalidated for key: {key}")
        else:
            logger.debug(f"Attempted to invalidate non-existent key: {key}")

    def clear(self) -> None:
        self._cache.clear()
        logger.info("InMemoryCache cleared")


class CacheManager:
    """Manages different caching strategies and provides a cache decorator."""

    def __init__(self, strategy: CacheStrategy = None):
        self._strategy = strategy if strategy else InMemoryCache()
        logger.info(f"CacheManager initialized with strategy: {type(self._strategy).__name__}")

    @property
    def strategy(self) -> CacheStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, new_strategy: CacheStrategy) -> None:
        if not isinstance(new_strategy, CacheStrategy):
            raise TypeError("Strategy must be an instance of CacheStrategy")
        self._strategy = new_strategy
        logger.info(f"CacheManager strategy updated to: {type(self._strategy).__name__}")

    def cache(self, ttl: Optional[int] = None, key_prefix: str = ""):
        """Decorator to cache the results of a function."""

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                # Generate a cache key based on function name and arguments
                # Simple serialization for args/kwargs
                # NOTE: For complex objects, a more robust serialization might be needed
                args_key = "-".join(map(str, args))
                kwargs_key = "-".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
                full_key = f"{key_prefix}{func.__name__}__{args_key}__{kwargs_key}"

                cached_result = self.strategy.get(full_key)
                if cached_result is not None:
                    logger.debug(f"Returning cached result for {func.__name__}")
                    return cached_result

                # If not in cache, call the original function and store the result
                logger.debug(f"Executing {func.__name__} and caching result")
                result = func(*args, **kwargs)
                self.strategy.set(full_key, result, ttl=ttl)
                return result
            return wrapper
        return decorator


# Example usage (for demonstration/testing)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)

    cache_manager = CacheManager(InMemoryCache(default_ttl=10))

    @cache_manager.cache(ttl=5, key_prefix="dashboard_data_")
    def get_dashboard_summary_data(user_id: int, report_type: str) -> Dict[str, Any]:
        logger.info("Simulating fetching dashboard summary data...")
        time.sleep(2)  # Simulate a long-running query
        return {"user_id": user_id, "report_type": report_type, "data": f"summary_data_for_{user_id}_{report_type}", "timestamp": time.time()}

    @cache_manager.cache(ttl=20)
    def get_individual_metric(metric_name: str) -> float:
        logger.info(f"Simulating fetching individual metric: {metric_name}...")
        time.sleep(1) # Simulate a query
        return time.time() * 100 % 1000 # dummy value

    print("\n--- First call (should compute and cache) ---")
    data1 = get_dashboard_summary_data(1, "daily")
    print(f"Data 1: {data1}")

    print("\n--- Second call (should be cached) ---")
    data2 = get_dashboard_summary_data(1, "daily")
    print(f"Data 2: {data2}")

    print("\n--- Call with different arguments (should compute and cache) ---")
    data3 = get_dashboard_summary_data(2, "monthly")
    print(f"Data 3: {data3}")

    print("\n--- Invalidate specific cache entry ---")
    cache_manager.strategy.invalidate("dashboard_data_get_dashboard_summary_data__1-daily__") # Manual invalidation
    data4 = get_dashboard_summary_data(1, "daily") # Should re-compute
    print(f"Data 4 (after invalidation): {data4}")

    print("\n--- Wait for cache to expire ---")
    print("Waiting 6 seconds for 'dashboard_data_get_dashboard_summary_data' cache to expire...")
    time.sleep(6) 
    data5 = get_dashboard_summary_data(1, "daily") # Should re-compute due to TTL
    print(f"Data 5 (after TTL expiry): {data5}")

    print("\n--- Testing individual metric cache ---")
    metric1 = get_individual_metric("sales_revenue")
    print(f"Metric 1: {metric1}")
    metric2 = get_individual_metric("sales_revenue")
    print(f"Metric 2 (cached): {metric2}")
    time.sleep(21) # wait for metric cache to expire
    metric3 = get_individual_metric("sales_revenue") # should recompute
    print(f"Metric 3 (after expiry): {metric3}")


    print("\n--- Clearing entire cache ---")
    cache_manager.strategy.clear()
    data6 = get_dashboard_summary_data(1, "daily") # Should re-compute
    print(f"Data 6 (after clear): {data6}")
