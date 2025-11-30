import os

# Global configuration settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
VPS_HOST = os.getenv("VPS_HOST", "localhost")
PORT = int(os.getenv("PORT", "8000"))

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
REGISTRY_DB_PATH = os.getenv("REGISTRY_DB_PATH", "data/registry.db")
APP_DB_PATH = os.getenv("APP_DB_PATH", "data/app.db")

# Upload settings
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "data/uploads")
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "16777216"))  # 16MB

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "data/app.log")