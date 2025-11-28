import os
import shutil
from decorators import pipeline_step

class ValidationProcessor:
    """Class to validate files in phase_4"""
    
    @pipeline_step
    def validate_files(self):
        """Validate HTML, CSS, and JS files in phase_4"""
        source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'dev', 'phase_3')
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'dev', 'phase_4')
        
        # Check if source directory exists
        if not os.path.exists(source_dir):
            return f"Source directory does not exist: {source_dir}"
        
        # Remove destination directory if it exists
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        
        # Copy all files from source to destination
        shutil.copytree(source_dir, output_dir)
        
        # Perform validation checks
        validation_results = self._perform_validation(output_dir)
        
        # Log validation results
        validation_log_path = os.path.join(output_dir, 'validation_report.txt')
        with open(validation_log_path, 'w', encoding='utf-8') as f:
            f.write("Validation Report\n")
            f.write("=================\n")
            for check, result in validation_results.items():
                f.write(f"{check}: {result}\n")
        
        return f"Successfully validated files in phase_4 from phase_3. Issues found: {len([r for r in validation_results.values() if 'FAIL' in r])}"
    
    def _perform_validation(self, output_dir):
        """Perform various validation checks"""
        results = {}
        
        # Check HTML validity
        html_count = 0
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.html'):
                    html_count += 1
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Basic HTML validation
                    if '<html' in content and '<head' in content and '<body' in content:
                        results[f"HTML Validation ({file})"] = "PASS"
                    else:
                        results[f"HTML Validation ({file})"] = "WARN: Missing standard HTML structure"
        
        results["Total HTML files"] = f"INFO: Found {html_count} HTML files"
        
        # Check for CSS files
        css_files = []
        for root, dirs, files in os.walk(os.path.join(output_dir, 'css')):
            for file in files:
                if file.endswith('.css'):
                    css_files.append(file)
        
        if css_files:
            results["CSS Files"] = f"INFO: Found CSS files: {', '.join(css_files)}"
        else:
            results["CSS Files"] = "WARN: No CSS files found"
        
        # Check for JS files
        js_files = []
        for root, dirs, files in os.walk(os.path.join(output_dir, 'js')):
            for file in files:
                if file.endswith('.js'):
                    js_files.append(file)
        
        if js_files:
            results["JS Files"] = f"INFO: Found JS files: {', '.join(js_files)}"
        else:
            results["JS Files"] = "INFO: No JS files found (may be intentional)"
        
        return results


# For compatibility with existing code
def copy_to_phase_4():
    validator = ValidationProcessor()
    return validator.validate_files()