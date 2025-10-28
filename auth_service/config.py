import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_key_for_dev')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db') # Default to SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_HOURS = 24
