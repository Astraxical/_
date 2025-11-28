import json
import os

class DataManager:
    """Class to handle data storage and retrieval"""
    
    def __init__(self, data_file="templates/jsons/alters.template.json"):
        self.data_file = data_file
    
    def save_data(self, data):
        """Save data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}
    
    def update_alter_info(self, alter_name, new_info):
        """Update information for a specific alter"""
        data = self.load_data()
        
        # Find the alter in the data structure
        # Note: This implementation assumes the data structure matches the template
        if "self" in data and data["self"]["name"] == alter_name:
            data["self"].update(new_info)
        elif "world" in data and "affinities" in data["world"]:
            # This would need to be customized based on actual data structure
            pass
        
        self.save_data(data)