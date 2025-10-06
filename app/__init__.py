from flask import Flask
from app.api.export_endpoint import financial_export_bp
import os

def create_app():
    app = Flask(__name__)

    # Load configuration from environment variables or a config file
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a_very_secret_key')
    # Other configurations like database URI can be set here

    # Register blueprints
    app.register_blueprint(financial_export_bp)

    return app
