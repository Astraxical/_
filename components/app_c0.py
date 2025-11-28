import os
import shutil
from flask import Flask
from jinja2 import Environment, FileSystemLoader
import json

def get_template_context():
    """Create sample context data for templates"""
    # Sample data based on the template structure
    sample_data = {
        "main_person": {
            "name": "Alex Smith",
            "description": "This is the main person in the system.",
            "age": 25,
            "gender": "Non-binary",
            "pronouns": ["they/them", "she/her"],
            "orientation": "Pansexual",
            "self_perception": "A person navigating life with multiple alters",
            "interests": ["Reading", "Coding", "Art", "Music"]
        },
        "alter1": {
            "self": {
                "name": "Taylor",
                "age": 22,
                "gender": "Female",
                "pronouns": ["she/her"],
                "orientation": "Lesbian",
                "self_perception": "A creative and artistic alter who loves music and art"
            },
            "affective": {
                "preferences": {
                    "mild": {
                        "likes": ["Art supplies", "Coffee", "Rainy days"],
                        "dislikes": ["Loud noises", "Crowds"]
                    },
                    "intense": {
                        "loves": ["Painting", "Live music", "Classic literature"],
                        "hates": ["Injustice", "Littering"]
                    }
                },
                "triggers": {
                    "positive": ["Creative space", "Favorite songs", "Quiet environments"],
                    "negative": ["Sudden loud sounds", "Being ignored", "Disorganization"]
                },
                "capacity": {
                    "social": "Prefers small groups",
                    "sensory": "Sensitive to bright lights",
                    "emotional_load": "Moderate"
                }
            },
            "relational": {
                "boundaries": {
                    "dm_request": "Open for creative collaborations",
                    "friend_request": "Requires mutual interest"
                }
            },
            "world": {
                "affinities": {
                    "toward": {
                        "media": {
                            "anime": ["Your Name", "Spirited Away"],
                            "movies": ["Amelie", "Her"],
                            "games": ["Gris", "Journey"],
                            "music": {
                                "artists": ["Lorde", "Florence + The Machine"],
                                "songs": ["Royals", "Dog Days Are Over"],
                                "genres": ["Indie", "Alternative"]
                            }
                        },
                        "aesthetic": {
                            "colors": ["Deep blues", "Earthy greens"],
                            "textures": ["Velvet", "Soft fabrics"],
                            "scents": ["Vanilla", "Lavender"],
                            "sounds": ["Gentle rain", "Piano music"]
                        },
                        "personal": {
                            "foods": ["Dark chocolate", "Fresh berries"],
                            "places": ["Art galleries", "Quiet libraries"],
                            "times_of_day": ["Evening", "Early morning"],
                            "words": ["Serendipity", "Ephemeral"]
                        },
                        "people": {
                            "cherished": ["Close friends", "Family"],
                            "trusted": ["Therapists", "Supportive peers"],
                            "tolerated": ["Acquaintances", "Coworkers"]
                        }
                    }
                }
            }
        },
        "alter2": {
            "self": {
                "name": "Jordan",
                "age": 28,
                "gender": "Male",
                "pronouns": ["he/him"],
                "orientation": "Asexual",
                "self_perception": "A protector alter who focuses on safety and structure"
            },
            "affective": {
                "preferences": {
                    "mild": {
                        "likes": ["Organization", "Planning", "Security"],
                        "dislikes": ["Chaos", "Unexpected changes"]
                    },
                    "intense": {
                        "loves": ["Productivity systems", "Routine", "Safety protocols"],
                        "hates": ["Negligence", "Unpredictable people"]
                    }
                },
                "triggers": {
                    "positive": ["Structured plans", "Clear rules", "Safe spaces"],
                    "negative": ["Disorganization", "Threatening situations", "Inconsistent behavior"]
                },
                "capacity": {
                    "social": "Comfortable in familiar groups",
                    "sensory": "Moderate sensitivity",
                    "emotional_load": "High"
                }
            },
            "relational": {
                "boundaries": {
                    "dm_request": "Open during safe hours",
                    "friend_request": "Requires introduction"
                }
            },
            "world": {
                "affinities": {
                    "toward": {
                        "media": {
                            "anime": ["Ghost in the Shell", "Attack on Titan"],
                            "movies": ["The Matrix", "Minority Report"],
                            "games": ["Deus Ex", "System Shock"],
                            "music": {
                                "artists": ["Nine Inch Nails", "Kraftwerk"],
                                "songs": ["Head Like a Hole", "The Robots"],
                                "genres": ["Industrial", "Electronic"]
                            }
                        },
                        "aesthetic": {
                            "colors": ["Dark blue", "Silver", "Black"],
                            "textures": ["Metal", "Hard surfaces"],
                            "scents": ["Mint", "Eucalyptus"],
                            "sounds": ["White noise", "Mechanical sounds"]
                        },
                        "personal": {
                            "foods": ["Protein-rich foods", "Energy bars"],
                            "places": ["Organized spaces", "Controlled environments"],
                            "times_of_day": ["Late night", "Early morning"],
                            "words": ["Protocol", "Efficiency"]
                        },
                        "people": {
                            "cherished": ["Family", "Trusted allies"],
                            "trusted": ["Security professionals", "System administrators"],
                            "tolerated": ["Acquaintances", "Colleagues"]
                        }
                    }
                },
                "gateway": ["Structured tasks", "Security protocols"]
            }
        }
    }
    return sample_data

def process_templates():
    """Process templates and generate static HTML files"""
    # Copy all files from webbuild/template/ to webbuild/dev/phase_0/
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'template')
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webbuild', 'dev', 'phase_0')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Copy all files from template dir to output dir
    if os.path.exists(template_dir):
        for item in os.listdir(template_dir):
            source_path = os.path.join(template_dir, item)
            dest_path = os.path.join(output_dir, item)

            if os.path.isfile(source_path):
                shutil.copy2(source_path, dest_path)
            elif os.path.isdir(source_path):
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                shutil.copytree(source_path, dest_path)

    # Process template files from templates/web/htmls/ and integrate into copied files
    html_templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'web', 'htmls')

    # Create Flask app to use its template engine
    app = Flask(__name__,
                template_folder=html_templates_dir,
                static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))

    # Configure the app to avoid URL building issues
    app.config['SERVER_NAME'] = 'localhost'

    # Get sample context
    context = get_template_context()

    # Process each template file
    for template_file in os.listdir(html_templates_dir):
        if template_file.endswith('.html'):
            try:
                # Render the template with context
                with app.app_context():
                    # Add alter1 and alter2 to context for card.alter.html
                    full_context = context.copy()
                    full_context['alter'] = context.get('alter1', {})
                    rendered_content = app.jinja_env.get_template(template_file).render(**full_context)

                # Write the processed content to the output directory
                output_file_path = os.path.join(output_dir, template_file)

                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(rendered_content)

            except Exception as e:
                print(f"Error processing template {template_file}: {str(e)}")
                continue

    return f"Processed templates from {html_templates_dir} and updated files in {output_dir}"

# For commandline execution
if __name__ == '__main__':
    print("Processing templates...")
    result = process_templates()
    print(result)