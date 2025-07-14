"""
Azure App Service Startup Script for Study Pal

This script initializes the Flask application for Azure App Service deployment.
It handles production configuration, environment variables, and proper WSGI setup.
"""

from app import app
import os

# Configure for production
if __name__ == "__main__":
    # Get port from environment variable (Azure sets this)
    port = int(os.environ.get('PORT', 8000))
    
    # Run with production settings
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,  # Disable debug in production
        threaded=True  # Enable threading for better performance
    ) 