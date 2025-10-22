import os
from dotenv import load_dotenv
from auth_service.app import create_app

load_dotenv() # Load environment variables from .env file

app = create_app()

if __name__ == '__main__':
    # Default to 5000 if not specified
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=port)
