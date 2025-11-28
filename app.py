from flask import Flask, render_template
import json
import os

def load_config():
    """Load configuration from config.toml"""
    import toml
    with open('config/config.toml', 'r') as f:
        return toml.load(f)

app = Flask(__name__)

# Load configuration
config = load_config()
app.config['SECRET_KEY'] = config['flask']['secret_key']

def load_alters_data():
    """Load the alters template data from JSON file"""
    import json
    with open('templates/jsons/alters.template.json', 'r') as f:
        return json.load(f)

def load_system_data():
    """Load the actual system data from a populated JSON file or create default structure"""
    import json
    import os

    # Try to load from a populated data file, fallback to template
    data_file = 'templates/jsons/bio.json'  # or wherever actual data will be stored
    template_file = 'templates/jsons/alters.template.json'

    # Check if populated data file exists
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            full_data = json.load(f)
    else:
        # Use template as base structure
        with open(template_file, 'r') as f:
            full_data = json.load(f)

    # Define the main person data from the template structure
    main_person = {
        "name": "Host",
        "description": "Main personality and host of the system",
        "interests": [],
        "age": full_data.get("self", {}).get("age", "Unknown"),
        "gender": full_data.get("self", {}).get("gender", "Unknown"),
        "pronouns": full_data.get("self", {}).get("pronouns", ["they/them"]),
        "orientation": full_data.get("self", {}).get("orientation", "Unknown"),
        "self_perception": full_data.get("self", {}).get("self_perception", "Unknown")
    }

    # Create alter profiles based on template structure without adding sample details
    alter1 = json.loads(json.dumps(full_data))  # Deep copy the template
    alter2 = json.loads(json.dumps(full_data))  # Deep copy the template

    return main_person, alter1, alter2

@app.route('/')
def index():
    main_person, alter1, alter2 = load_system_data()
    return render_template('htmls/base.html',
                           main_person=main_person,
                           alter1=alter1,
                           alter2=alter2)

@app.route('/alter/<name>')
def alter_profile(name):
    """Show individual alter profile page"""
    main_person, alter1, alter2 = load_system_data()

    # This would be updated when real alter names are available
    # For now, return a generic response since we don't have specific alter names
    return render_template('htmls/base.html',
                           main_person=main_person,
                           alter1=alter1,
                           alter2=alter2,
                           selected_alter=None)

if __name__ == '__main__':
    try:
        app.run(
            debug=config['flask']['debug'],
            host=config['flask']['host'],
            port=config['flask']['port']
        )
    except Exception as e:
        print(f"Error starting app: {e}")