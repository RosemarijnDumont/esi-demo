from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    Session(app) # Initialize Flask-Session

    with app.app_context():
        from .api.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')

        db.create_all() # Create database tables for our models

    return app
