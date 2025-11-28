import os
import json
import shutil
from decorators import pipeline_step

class AlterDataInjector:
    """Class to inject alter data from database/alters.json into the website"""
    
    @pipeline_step
    def inject_alter_data(self):
        """Inject alter data from database/alters.json into the website in phase_3"""
        # Get paths
        source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'dev', 'phase_2')
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'dev', 'phase_3')
        alters_json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'alters.json')
        
        # Check if source directory exists
        if not os.path.exists(source_dir):
            return f"Source directory does not exist: {source_dir}"
        
        # Check if alters.json exists
        if not os.path.exists(alters_json_path):
            return f"Alters JSON file does not exist: {alters_json_path}"
        
        # Remove destination directory if it exists
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        
        # Copy all files from source to destination first
        shutil.copytree(source_dir, output_dir)
        
        # Read the alters data
        with open(alters_json_path, 'r', encoding='utf-8') as f:
            alters_data = json.load(f)
        
        # Update HTML files to inject alter data
        self._inject_data_into_files(output_dir, alters_data)
        
        return f"Successfully injected alter data into phase_3 from phase_2"
    
    def _inject_data_into_files(self, output_dir, alters_data):
        """Helper method to inject alter data into HTML files"""
        # Read the index.html and update it to include alter cards
        index_path = os.path.join(output_dir, 'index.html')
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate alter cards HTML
            alter_cards_html = self._generate_alter_cards(alters_data)
            
            # Replace placeholder with alter cards, or add them after the header
            if '<!-- ALTER CARDS PLACEHOLDER -->' in content:
                content = content.replace('<!-- ALTER CARDS PLACEHOLDER -->', alter_cards_html)
            elif '<div class="container">' in content:
                # Insert alter cards after the container div
                content = content.replace('<div class="container">', f'<div class="container"><h2>Alters</h2>{alter_cards_html}', 1)
            else:
                # Append to the content
                content += f'<div class="alters-container">{alter_cards_html}</div>'
            
            # Write updated content back to file
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    def _generate_alter_cards(self, alters_data):
        """Generate HTML for alter cards"""
        cards_html = '<div class="alters-grid">'
        
        for alter in alters_data:
            name = alter.get('self', {}).get('name', 'Unknown')
            age = alter.get('self', {}).get('age', 'N/A')
            gender = alter.get('self', {}).get('gender', 'N/A')
            pronouns = ', '.join(alter.get('self', {}).get('pronouns', []))
            orientation = alter.get('self', {}).get('orientation', 'N/A')
            self_perception = alter.get('self', {}).get('self_perception', 'N/A')
            
            likes = alter.get('affective', {}).get('preferences', {}).get('mild', {}).get('likes', [])
            dislikes = alter.get('affective', {}).get('preferences', {}).get('mild', {}).get('dislikes', [])
            colors = alter.get('world', {}).get('affinities', {}).get('toward', {}).get('aesthetic', {}).get('colors', [])
            
            card_html = f'''
            <div class="alter-card">
                <h3>{name}</h3>
                <p><strong>Age:</strong> {age if age else "N/A"}</p>
                <p><strong>Gender:</strong> {gender}</p>
                <p><strong>Pronouns:</strong> {pronouns}</p>
                <p><strong>Orientation:</strong> {orientation}</p>
                <p><strong>Self Perception:</strong> {self_perception}</p>
            '''
            
            if likes:
                card_html += f'<p><strong>Likes:</strong> {", ".join(likes)}</p>'
            
            if dislikes:
                card_html += f'<p><strong>Dislikes:</strong> {", ".join(dislikes)}</p>'
            
            if colors:
                card_html += f'<p><strong>Favorite Colors:</strong> {", ".join(colors)}</p>'
            
            card_html += '</div>'
            
            cards_html += card_html
        
        cards_html += '</div>'
        
        return cards_html


# For compatibility with existing code
def copy_to_phase_3():
    injector = AlterDataInjector()
    return injector.inject_alter_data()