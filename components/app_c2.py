import os
import shutil
from decorators import pipeline_step

class CSSStyler:
    """Class to enhance CSS styling in phase_2"""
    
    @pipeline_step
    def enhance_css_styling(self):
        """Enhance CSS styling in phase_2"""
        source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'dev', 'phase_1')
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'dev', 'phase_2')
        
        # Check if source directory exists
        if not os.path.exists(source_dir):
            return f"Source directory does not exist: {source_dir}"
        
        # Remove destination directory if it exists
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        
        # Copy all files from source to destination
        shutil.copytree(source_dir, output_dir)
        
        # Enhance CSS if style.css exists
        css_dir = os.path.join(output_dir, 'css')
        if os.path.exists(css_dir):
            style_css_path = os.path.join(css_dir, 'style.css')
            if os.path.exists(style_css_path):
                with open(style_css_path, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                
                # Add alter-specific CSS styling
                enhanced_css_content = self._enhance_css_content(css_content)
                
                # Write updated content back
                with open(style_css_path, 'w', encoding='utf-8') as f:
                    f.write(enhanced_css_content)
        
        return f"Successfully enhanced CSS styling in phase_2 from phase_1"
    
    def _enhance_css_content(self, original_content):
        """Enhance CSS content with additional styling for alters"""
        additional_css = """
/* Alter-specific styling */
.alter-card {
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    margin: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
    min-height: 300px;
}

.alter-card:hover {
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    transform: translateY(-2px);
}

.alter-card.active {
    border-color: #4a6fa5;
    background-color: #f0f8ff;
}

.alters-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    padding: 20px 0;
}

.alters-container {
    margin-top: 20px;
}

/* Enhanced styling for profile cards */
.profile-card {
    background-color: #f9f9f9;
    padding: 1.5rem;
    border-radius: 8px;
    border-left: 4px solid #4a6fa5;
    margin-bottom: 1.5rem;
}

/* Individual alter card styling */
.astral-card {
    border-left: 5px solid #808080; /* Gray for Astral's "Shades of Gray" */
    background: linear-gradient(to bottom, #f0f0f0, #ffffff);
}

.dexen-card {
    border-left: 5px solid #000080; /* Blue for Dexen */
    background: linear-gradient(to bottom, #e6f0ff, #ffffff);
}

.seles-card {
    border-left: 5px solid #d3d3d3; /* Light gray for Seles */
    background: linear-gradient(to bottom, #f0f0f0, #ffffff);
}

/* Additional responsive design */
@media (max-width: 768px) {
    .alters-grid {
        grid-template-columns: 1fr;
    }

    .alter-card {
        min-height: auto;
    }
}
"""

        # Combine the original content with the enhanced styling
        return original_content + "\n" + additional_css


# For compatibility with existing code
def copy_to_phase_2():
    styler = CSSStyler()
    return styler.enhance_css_styling()