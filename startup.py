"""
Azure App Service Startup Script for Study Pal

This script initializes the Flask application for Azure App Service deployment.
It handles production configuration, environment variables, and proper WSGI setup.
"""

import os
import sys

# Ensure we're in the correct directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Add current directory to Python path
sys.path.insert(0, script_dir)

# Debug: Print current working directory and file structure
print(f"Current working directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")
if os.path.exists('templates'):
    print(f"Templates found: {os.listdir('templates')}")
else:
    print("Templates directory not found!")

from app import app

# Get port from environment variable (Azure sets this)
port = int(os.environ.get('PORT', 8000))

# Configure for production
if __name__ == "__main__":
    # Run with production settings
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,  # Disable debug in production
        threaded=True  # Enable threading for better performance
    )
else:
    # Production mode (when called by gunicorn)
    application = app
