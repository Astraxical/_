import os
import shutil
from decorators import pipeline_step

class JavaScriptProcessor:
    """Class to enhance JavaScript functionality in phase_1"""
    
    @pipeline_step
    def enhance_javascript(self):
        """Enhance JavaScript functionality in phase_1"""
        source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'dev', 'phase_0')
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'dev', 'phase_1')
        
        # Check if source directory exists
        if not os.path.exists(source_dir):
            return f"Source directory does not exist: {source_dir}"
        
        # Remove destination directory if it exists
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        
        # Copy all files from source to destination
        shutil.copytree(source_dir, output_dir)
        
        # Enhance JavaScript functionality if main.js exists
        js_dir = os.path.join(output_dir, 'js')
        if os.path.exists(js_dir):
            main_js_path = os.path.join(js_dir, 'main.js')
            if os.path.exists(main_js_path):
                with open(main_js_path, 'r', encoding='utf-8') as f:
                    js_content = f.read()
                
                # Add alter-specific JavaScript functionality
                enhanced_js_content = self._enhance_javascript_content(js_content)
                
                # Write updated content back
                with open(main_js_path, 'w', encoding='utf-8') as f:
                    f.write(enhanced_js_content)
        
        # Also update HTML files to potentially include JavaScript enhancements
        self._enhance_html_files(output_dir)
        
        return f"Successfully enhanced JavaScript functionality in phase_1 from phase_0"
    
    def _enhance_javascript_content(self, original_content):
        """Enhance JavaScript content with additional functionality"""
        additional_js = """
// Alter-specific JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners for alter cards
    const alterCards = document.querySelectorAll('.alter-card');
    alterCards.forEach(card => {
        card.addEventListener('click', function() {
            // Add interactivity for alter cards
            this.classList.toggle('active');
        });
    });
    
    // Implement search and filter functionality for alters
    setupAlterSearch();
    
    // Continue the original functionality
    setupNavigation();
});

function setupAlterSearch() {
    // Add search functionality for alters
    console.log('Alter search functionality initialized');
}

function setupNavigation() {
    // Add smooth scrolling for navigation links
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Refresh iframes if needed
    document.querySelectorAll('iframe').forEach(iframe => {
        iframe.addEventListener('load', function() {
            // Optional: Add any iframe loaded functionality here
            console.log('Iframe loaded:', iframe.src);
        });
    });
}
"""
        
        # Combine the original content with the enhanced functionality
        return original_content + "\n" + additional_js
    
    def _enhance_html_files(self, output_dir):
        """Enhance HTML files with JavaScript-related attributes"""
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Add any HTML enhancements needed for JavaScript
                    if '<body>' in content:
                        content = content.replace('<body>', '<body class="js-enhanced">', 1)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)


# For compatibility with existing code
def copy_to_phase_1():
    processor = JavaScriptProcessor()
    return processor.enhance_javascript()