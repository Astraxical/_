import os
import sys
from flask import Flask, send_from_directory, abort
import toml
from decorators import pipeline_step
from phase_enum import Phase

class Pipeline:
    """Main pipeline class to process all phases"""

    @pipeline_step
    def run_pipeline(self):
        """Run the entire pipeline from HTML processing through to production"""
        # Phase 0: HTML processing
        from components.app_c0 import process_phase_0
        result_0 = process_phase_0()

        # Phase 1: JavaScript enhancement
        from components.app_c1 import copy_to_phase_1
        result_1 = copy_to_phase_1()

        # Phase 2: CSS styling enhancement
        from components.app_c2 import copy_to_phase_2
        result_2 = copy_to_phase_2()

        # Phase 3: Alter data injection
        from components.app_c3 import copy_to_phase_3
        result_3 = copy_to_phase_3()

        # Phase 4: Validation
        from components.app_c4 import copy_to_phase_4
        result_4 = copy_to_phase_4()

        # Phase 5: Minification
        from components.app_c5 import copy_to_phase_5
        result_5 = copy_to_phase_5()

        # Production: Deploy to production
        from components.app_c6 import copy_to_production
        result_prod = copy_to_production()

        return {
            Phase.HTML: result_0,
            Phase.JAVASCRIPT: result_1,
            Phase.CSS: result_2,
            Phase.ALTER_DATA: result_3,
            Phase.VALIDATION: result_4,
            Phase.MINIFICATION: result_5,
            Phase.PRODUCTION: result_prod
        }


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
            pipeline = Pipeline()
            results = pipeline.run_pipeline()
            
            response = "Pipeline processing completed:\n"
            for phase, result in results.items():
                response += f"{phase.name}: {result}\n"
            
            return response
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
            index_path = os.path.join(app.root_path, 'webbuild', 'dev', 'phase_0', 'index.html')
            if os.path.exists(index_path):
                return send_from_directory('webbuild/dev/phase_0', 'index.html')
            else:
                return "No index.html file found in webbuild/dev/phase_0/"
        elif phase == '1':
            # Serve index.html from webbuild/dev/phase_1/
            index_path = os.path.join(app.root_path, 'webbuild', 'dev', 'phase_1', 'index.html')
            if os.path.exists(index_path):
                return send_from_directory('webbuild/dev/phase_1', 'index.html')
            else:
                return "No index.html file found in webbuild/dev/phase_1/"
        elif phase == '2':
            # Serve index.html from webbuild/dev/phase_2/
            index_path = os.path.join(app.root_path, 'webbuild', 'dev', 'phase_2', 'index.html')
            if os.path.exists(index_path):
                return send_from_directory('webbuild/dev/phase_2', 'index.html')
            else:
                return "No index.html file found in webbuild/dev/phase_2/"
        elif phase == '3':
            # Serve index.html from webbuild/dev/phase_3/
            index_path = os.path.join(app.root_path, 'webbuild', 'dev', 'phase_3', 'index.html')
            if os.path.exists(index_path):
                return send_from_directory('webbuild/dev/phase_3', 'index.html')
            else:
                return "No index.html file found in webbuild/dev/phase_3/"
        elif phase == '4':
            # Serve index.html from webbuild/dev/phase_4/
            index_path = os.path.join(app.root_path, 'webbuild', 'dev', 'phase_4', 'index.html')
            if os.path.exists(index_path):
                return send_from_directory('webbuild/dev/phase_4', 'index.html')
            else:
                return "No index.html file found in webbuild/dev/phase_4/"
        elif phase == '5':
            # Serve index.html from webbuild/dev/phase_5/
            index_path = os.path.join(app.root_path, 'webbuild', 'dev', 'phase_5', 'index.html')
            if os.path.exists(index_path):
                return send_from_directory('webbuild/dev/phase_5', 'index.html')
            else:
                return "No index.html file found in webbuild/dev/phase_5/"
        elif phase == 'production':
            # Serve index.html from webbuild/production/
            index_path = os.path.join(app.root_path, 'webbuild', 'production', 'index.html')
            if os.path.exists(index_path):
                return send_from_directory('webbuild/production', 'index.html')
            else:
                return "No index.html file found in webbuild/production/"
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

        if phase in ['0', '1', '2', '3', '4', '5', 'production'] and type_ and name:
            # Build the file extension based on the type
            if type_ == 'css':
                extension = 'css'
            elif type_ == 'js':
                extension = 'js'
            else:
                extension = 'html'  # default for html and other types

            # Build path to requested asset in the appropriate phase directory
            if phase == 'production':
                abs_asset_path = os.path.join(app.root_path, 'webbuild', 'production', type_, f'{name}.{extension}')
                if os.path.exists(abs_asset_path):
                    # Serve the specific file from production
                    return send_from_directory(f'webbuild/production/{type_}', f'{name}.{extension}')
                else:
                    abort(404)
            else:
                # For regular dev phases
                abs_asset_path = os.path.join(app.root_path, 'webbuild', 'dev', f'phase_{phase}', type_, f'{name}.{extension}')
                if os.path.exists(abs_asset_path):
                    # Serve the specific file from the appropriate phase
                    return send_from_directory(f'webbuild/dev/phase_{phase}/{type_}', f'{name}.{extension}')
                else:
                    abort(404)
        else:
            return "Missing required parameters: phase, type, name"

    # Individual phase endpoints
    @app.route('/dev/phase0')
    def dev_phase_0():
        return send_from_directory('webbuild/dev/phase_0', 'index.html')

    @app.route('/dev/phase1')
    def dev_phase_1():
        return send_from_directory('webbuild/dev/phase_1', 'index.html')

    @app.route('/dev/phase2')
    def dev_phase_2():
        return send_from_directory('webbuild/dev/phase_2', 'index.html')

    @app.route('/dev/phase3')
    def dev_phase_3():
        return send_from_directory('webbuild/dev/phase_3', 'index.html')

    @app.route('/dev/phase4')
    def dev_phase_4():
        return send_from_directory('webbuild/dev/phase_4', 'index.html')

    @app.route('/dev/phase5')
    def dev_phase_5():
        return send_from_directory('webbuild/dev/phase_5', 'index.html')

    @app.route('/dev/production')
    def dev_production():
        return send_from_directory('webbuild/production', 'index.html')

    @app.route('/production')
    def production():
        return send_from_directory('webbuild/production', 'index.html')
    
    return app

# For command-line execution
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'process':
        # Process templates when called with 'process' argument
        # This runs the entire pipeline
        pipeline = Pipeline()
        results = pipeline.run_pipeline()
        
        print(f"Pipeline processing completed:")
        for phase, result in results.items():
            print(f"{phase.name}: {result}")
    else:
        # Run as web server
        app = create_app()
        app.run(
            host=app.config.get('HOST', '0.0.0.0'),
            port=app.config.get('PORT', 5000),
            debug=app.config.get('DEBUG', False)
        )