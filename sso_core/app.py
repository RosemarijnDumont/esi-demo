
from flask import Flask, jsonify
from sso_core.api.sso import sso_bp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(sso_bp, url_prefix='/api/v1/sso')

    @app.route('/')
    def hello_world():
        return 'SSO Core Service is running!'

    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"404 Not Found: {request.path}")
        return jsonify({'error': 'Not Found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"500 Internal Server Error: {error}")
        return jsonify({'error': 'Internal Server Error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
