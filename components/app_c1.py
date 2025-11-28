# Component for handling alter data

class AlterManager:
    """Class to manage information about alters"""
    
    def __init__(self):
        self.alters = []
    
    def add_alter(self, alter_data):
        """Add a new alter to the system"""
        self.alters.append(alter_data)
    
    def get_alter_by_name(self, name):
        """Get alter information by name"""
        for alter in self.alters:
            if alter.get('name') == name:
                return alter
        return None
    
    def get_all_alters(self):
        """Get all alters in the system"""
        return self.alters


# Example usage
if __name__ == "__main__":
    manager = AlterManager()
    
    # Add example alters
    manager.add_alter({
        "name": "Riley",
        "description": "The creative and artistic alter",
        "interests": ["Drawing", "Music", "Writing"],
        "pronouns": "she/her"
    })
    
    manager.add_alter({
        "name": "Jordan",
        "description": "The protective and logical alter",
        "interests": ["Strategy games", "Problem solving", "Security"],
        "pronouns": "he/him"
    })
    
    print("Number of alters:", len(manager.get_all_alters()))