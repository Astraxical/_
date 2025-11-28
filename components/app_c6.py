import os
import shutil
from decorators import pipeline_step

class ProductionPusher:
    """Class to push files from phase_5 to production"""
    
    @pipeline_step
    def copy_to_production(self):
        """Copy all files from webbuild/dev/phase_5 to webbuild/production/"""
        source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'dev', 'phase_5')
        dest_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'production')
        
        # Check if source directory exists
        if not os.path.exists(source_dir):
            return f"Source directory does not exist: {source_dir}"
        
        # Remove destination directory if it exists
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        
        # Create destination directory
        os.makedirs(dest_dir, exist_ok=True)
        
        # Copy all files from source to destination
        for item in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item)
            dest_path = os.path.join(dest_dir, item)
            
            if os.path.isfile(source_path):
                shutil.copy2(source_path, dest_path)
            elif os.path.isdir(source_path):
                shutil.copytree(source_path, dest_path)
        
        return f"Successfully copied files from phase_5 to production"


# For compatibility with existing code
def copy_to_production():
    pusher = ProductionPusher()
    return pusher.copy_to_production()