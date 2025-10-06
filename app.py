
from flask import Flask
from auth_routes import auth_bp
import os
import logging

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix="/auth")

# Configure logging for the application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route("/", methods=["GET"])
def health_check():
    logging.info("Health check endpoint hit.")
    return "Authentication Service is Up and Running!", 200

if __name__ == "__main__":
    # Set a default secret key for development, use environment variable in production
    os.environ.setdefault("JWT_SECRET_KEY", "a_very_secret_key_that_should_be_in_env_in_prod")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
