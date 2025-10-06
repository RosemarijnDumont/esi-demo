# auth_service/app/__init__.py
from flask import Flask
from .routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
