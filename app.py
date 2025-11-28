import os
import sys
from flask import Flask, send_from_directory, abort
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

    @app.route('/dev')
    def dev_phase():
        """
        Serve files from webbuild/dev/phase_0/ directory based on phase parameter
        """
        import flask
        phase = flask.request.args.get('phase')

        if phase == '0':
            # Serve index.html from webbuild/dev/phase_0/
            phase_0_dir = os.path.join(app.root_path, 'webbuild', 'dev', 'phase_0')
            index_path = os.path.join(phase_0_dir, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory('webbuild/dev/phase_0', 'index.html')
            else:
                return "No index.html file found in webbuild/dev/phase_0/"
        else:
            return f"Phase {phase} not found"

    @app.route('/assets')
    def assets():
        """
        Serve specific asset files based on phase, type, and name parameters
        """
        import flask
        phase = flask.request.args.get('phase')
        type_ = flask.request.args.get('type')
        name = flask.request.args.get('name')

        if phase == '0' and type_ and name:
            # Build path to requested asset in webbuild/dev/phase_0/
            asset_path = os.path.join('webbuild', 'dev', f'phase_{phase}', type_, f'{name}.html')

            # Check if the file exists
            abs_asset_path = os.path.join(app.root_path, 'webbuild', 'dev', f'phase_{phase}', type_, f'{name}.html')
            if os.path.exists(abs_asset_path):
                # Serve the specific file
                return send_from_directory(f'webbuild/dev/phase_{phase}/{type_}', f'{name}.html')
            else:
                abort(404)
        else:
            return "Missing required parameters: phase, type, name"

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