# This file can be used for additional configuration if needed, e.g., secret keys, database URIs.
# For now, API keys are loaded directly from environment variables in app.py for simplicity and security.

class Config:
    """Base configuration."""
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    pass
