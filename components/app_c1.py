import os
import shutil

def copy_to_phase_1():
    """Copy all files from webbuild/dev/phase_0 to webbuild/dev/phase_1"""
    source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'dev', 'phase_0')
    dest_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'dev', 'phase_1')
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        return f"Source directory does not exist: {source_dir}"
    
    # Remove destination directory if it exists
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    # Copy all files from source to destination
    shutil.copytree(source_dir, dest_dir)
    
    return f"Successfully copied files from phase_0 to phase_1"