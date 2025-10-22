from flask import Flask, jsonify
import logging
from logging.handlers import RotatingFileHandler
import os

from auth_service.app.api.auth_routes import auth_bp
from auth_service.app.exceptions import InvalidUsage

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_super_secret_key') # Use a strong, unique key in production
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=24) # Example, adjust as needed
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    # Logging setup
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/auth_service.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Authentication Service startup')

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Error Handler
    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'message': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.exception('An internal server error occurred')
        return jsonify({'message': 'Internal server error'}), 500

    return app

# This is added for local development/testing convenience
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    app = create_app()
    app.run(debug=True, port=5000)

import datetime
