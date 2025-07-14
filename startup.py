"""
Azure App Service Startup Script for Study Pal

This script initializes the Flask application for Azure App Service deployment.
It handles production configuration, environment variables, and proper WSGI setup.
"""

import os
import sys

# Get port from environment variable (Azure sets this)
port = int(os.environ.get('PORT', 8000))

# For Azure App Service, use gunicorn
if __name__ == "__main__":
    # Development mode
    from app import app
    app.run(host='0.0.0.0', port=port, debug=False)
else:
    # Production mode (when called by gunicorn)
    from app import app
    application = app
