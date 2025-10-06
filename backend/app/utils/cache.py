from flask_caching import Cache

cache = Cache()

def init_cache(app):
    cache.init_app(app, config={
        "CACHE_TYPE": "redis",  # Use Redis for production caching
        "CACHE_REDIS_HOST": "localhost",
        "CACHE_REDIS_PORT": "6379",
        "CACHE_REDIS_DB": "0",
        "CACHE_REDIS_URL": "redis://localhost:6379/0",
        "CACHE_DEFAULT_TIMEOUT": 300 # Default cache timeout in seconds
    })
