# Codebase Directory

This directory contains all the actual implementation files of the Multi-House Application.

For project documentation and planning files, please refer to the parent directory.

## Quick Navigation
- [Main Application](./main.py): The application entry point
- [Components](./components/): Integration layer between modules and app
- [Modules](./modules/): Autonomous "houses" (forums, rtc, template, admin)
- [Global Templates](./templates/): Base layouts and fallbacks
- [Static Assets](./static/): Site-wide CSS, JS, and assets
- [Utilities](./utils/): Helper functions and database utilities
- [Deployment](./deploy/): Startup scripts

## Running the Application

From this directory:
1. Install dependencies: `pip install -r requirements.txt`
2. Initialize the database: `python init_db.py`
3. Run the application: `uvicorn main:app --reload`