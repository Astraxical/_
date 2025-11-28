import os
import sys
from flask import Flask
import toml
from components.app_c0 import process_templates

def create_app():
    app = Flask(__name__,
                template_folder='templates/web/htmls',
                static_folder='static')
    
    # Load configuration from TOML file
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.toml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = toml.load(f)
        
        # Configure Flask app from config
        flask_config = config.get('flask', {})
        for key, value in flask_config.items():
            app.config[key.upper()] = value
        
        # Set default secret key if not provided
        if 'SECRET_KEY' not in app.config:
            app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    @app.route('/')
    def index():
        return "Template Processing Application"
    
    @app.route('/process')
    def process():
        try:
            result = process_templates()
            return f"Template processing completed: {result}"
        except Exception as e:
            return f"Error processing templates: {str(e)}"
    
    return app

# For command-line execution
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'process':
        # Process templates when called with 'process' argument
        result = process_templates()
        print(f"Template processing completed: {result}")
    else:
        # Run as web server
        app = create_app()
        app.run(
            host=app.config.get('HOST', '0.0.0.0'),
            port=app.config.get('PORT', 5000),
            debug=app.config.get('DEBUG', False)
        )