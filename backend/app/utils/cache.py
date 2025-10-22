from flask_caching import Cache

cache = Cache()

def init_cache(app):
    """
    Initializes Flask-Caching with application configuration.
    """
    cache.init_app(app)
