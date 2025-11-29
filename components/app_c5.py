import os
import shutil
import re
from decorators import pipeline_step

class MinificationProcessor:
    """Class to minify files in phase_5"""
    
    @pipeline_step
    def minify_files(self):
        """Minify HTML, CSS, and JS files in phase_5"""
        source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'dev', 'phase_4')
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'dev', 'phase_5')
        
        # Check if source directory exists
        if not os.path.exists(source_dir):
            return f"Source directory does not exist: {source_dir}"
        
        # Remove destination directory if it exists
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        
        # Copy all files from source to destination
        shutil.copytree(source_dir, output_dir)
        
        # Minify files
        html_count, css_count, js_count = self._minify_all_files(output_dir)
        
        return f"Successfully minified files in phase_5 from phase_4. Minified: {html_count} HTML, {css_count} CSS, {js_count} JS files"
    
    def _minify_all_files(self, output_dir):
        """Minify all HTML, CSS, and JS files in the directory"""
        html_count = 0
        css_count = 0
        js_count = 0
        
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                
                if file.endswith('.html'):
                    self._minify_html_file(file_path)
                    html_count += 1
                elif file.endswith('.css'):
                    self._minify_css_file(file_path)
                    css_count += 1
                elif file.endswith('.js'):
                    self._minify_js_file(file_path)
                    js_count += 1
        
        return html_count, css_count, js_count
    
    def _minify_html_file(self, file_path):
        """Minify an HTML file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove comments
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        
        # Remove extra whitespace while preserving structure
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r'>\s+<', '><', content)
        content = content.strip()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _minify_css_file(self, file_path):
        """Minify a CSS file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Remove whitespace
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r'\s*{\s*', '{', content)
        content = re.sub(r'\s*}\s*', '}', content)
        content = re.sub(r'\s*;\s*', ';', content)
        content = re.sub(r'\s*:\s*', ':', content)
        content = re.sub(r'\s*,\s*', ',', content)
        content = content.strip()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _minify_js_file(self, file_path):
        """Minify a JS file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove comments (both single-line and multi-line)
        # This is a simplified minification - in a real scenario, we'd need a proper JS parser
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r'\s*{\s*', '{', content)
        content = re.sub(r'\s*}\s*', '}', content)
        content = re.sub(r'\s*;\s*', ';', content)
        content = re.sub(r'\s*:\s*', ':', content)
        content = re.sub(r'\s*,\s*', ',', content)
        content = content.strip()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)


# For compatibility with existing code
def copy_to_phase_5():
    minifier = MinificationProcessor()
    return minifier.minify_files()