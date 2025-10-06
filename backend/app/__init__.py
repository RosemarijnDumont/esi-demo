from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.app.utils.cache import init_cache
from backend.app.routes.reports import reports_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db' # Replace with your actual DB URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    init_cache(app)  # Initialize caching

    app.register_blueprint(reports_bp, url_prefix='/api')

    return app
