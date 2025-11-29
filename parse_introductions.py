import json
import re
import os
from typing import Dict, List, Any

def parse_mx_file(file_path: str) -> Dict[str, Any]:
    """Parse an .mx file and extract information into a structured format."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Initialize with the template structure
    alter_data = {
        "self": {
            "name": "",
            "age": None,
            "gender": "",
            "pronouns": [],
            "orientation": "",
            "self_perception": ""
        },
        "affective": {
            "preferences": {
                "mild": {
                    "likes": [],
                    "dislikes": []
                },
                "intense": {
                    "loves": [],
                    "hates": []
                }
            },
            "triggers": {
                "positive": [],
                "negative": []
            },
            "capacity": {
                "social": "",
                "sensory": "",
                "emotional_load": ""
            }
        },
        "relational": {
            "boundaries": {
                "dm_request": "",
                "friend_request": ""
            }
        },
        "world": {
            "affinities": {
                "toward": {
                    "media": {
                        "anime": [],
                        "movies": [],
                        "games": [],
                        "music": {
                            "artists": [],
                            "songs": [],
                            "genres": []
                        }
                    },
                    "aesthetic": {
                        "colors": [],
                        "textures": [],
                        "scents": [],
                        "sounds": []
                    },
                    "personal": {
                        "foods": [],
                        "places": [],
                        "times_of_day": [],
                        "words": []
                    },
                    "people": {
                        "cherished": [],
                        "trusted": [],
                        "tolerated": []
                    }
                },
                "away": {
                    "media": {
                        "anime": [],
                        "movies": [],
                        "games": [],
                        "music": {
                            "artists": [],
                            "songs": [],
                            "genres": []
                        }
                    },
                    "aesthetic": {
                        "colors": [],
                        "textures": [],
                        "scents": [],
                        "sounds": []
                    },
                    "personal": {
                        "foods": [],
                        "places": [],
                        "times_of_day": [],
                        "words": []
                    },
                    "people": {
                        "distrusted": [],
                        "feared": [],
                        "rejected": []
                    }
                }
            },
            "gateway": []
        }
    }

    # Extract name (handle both formats: Name: value and ღ Name ღ : value)
    name_match = re.search(r'(?:[Nn]ame|[\u10e6\u10e7]\s*[Nn]ame\s*[\u10e6\u10e7])[^:]*:?\s*([^\n\r]+)', content)
    if name_match:
        alter_data["self"]["name"] = name_match.group(1).strip()

    # Extract pronouns
    pronouns_match = re.search(r'(?:[Pp]ronoun|Pronouns|[\u10e6\u10e7]\s*[Pp]ronouns\s*[\u10e6\u10e7])[^:]*:?\s*([^\n\r]+)', content)
    if pronouns_match:
        pronouns_text = pronouns_match.group(1).strip()
        # Split by slash, comma, or 'and' to get individual pronouns
        pronouns = re.split(r'[\/,]', pronouns_text)
        alter_data["self"]["pronouns"] = [p.strip() for p in pronouns if p.strip()]

    # Extract age
    age_match = re.search(r'(?:[Aa]ge|[\u10e6\u10e7]\s*[Aa]ge\s*[\u10e6\u10e7])[^:]*:?\s*(\d+)', content)
    if age_match:
        alter_data["self"]["age"] = int(age_match.group(1))

    # Extract gender
    gender_match = re.search(r'(?:[Gg]ender|Gender|[\u10e6\u10e7]\s*[Gg]ender\s*[\u10e6\u10e7])[^:]*:?\s*([^\n\r]+)', content)
    if gender_match:
        alter_data["self"]["gender"] = gender_match.group(1).strip()

    # Extract orientation
    orientation_match = re.search(r'(?:[Oo]rientation|Orientation|[\u10e6\u10e7]\s*[Oo]rientation\s*[\u10e6\u10e7])[^:]*:?\s*([^\n\r]+)', content)
    if orientation_match:
        alter_data["self"]["orientation"] = orientation_match.group(1).strip()

    # Extract likes - look for various patterns
    # Pattern 1: ღ Likes ღ : (list with bullets)
    likes_pattern1 = re.search(r'(?:[Ll]ikes|[\u10e6\u10e7]\s*[Ll]ikes\s*[\u10e6\u10e7])[^:]*:?\s*(.*?)(?=\n(?:[^:\n]*\n)?(?:[Dd]islikes|DNI|Boundaries|•『♡』•|└|┗|┆|┇|☆|$))', content, re.DOTALL)

    if not likes_pattern1:
        # Pattern 2: Just look for likes section
        likes_pattern1 = re.search(r'[Ll]ikes[^:]*:?\s*(.*?)(?=\n[LlDd]|$)', content, re.DOTALL)

    if likes_pattern1:
        likes_text = likes_pattern1.group(1).strip()
        # Extract individual likes from bullet points
        likes_items = re.findall(r'[•\u2022]\s*([^\n\r]+)', likes_text)
        alter_data["affective"]["preferences"]["mild"]["likes"] = [item.strip().rstrip('.') for item in likes_items if item.strip()]

    # Extract dislikes - look for various patterns
    # Pattern 1: ღ Dislikes ღ : (list with bullets)
    dislikes_pattern1 = re.search(r'(?:[Dd]islikes|[\u10e6\u10e7]\s*[Dd]islikes\s*[\u10e6\u10e7])[^:]*:?\s*(.*?)(?=\n(?:[^:\n]*\n)?(?:[Ll]ikes|[Bb]oundaries|•『♡』•|└|┗|┆|┇|☆|$))', content, re.DOTALL)

    if not dislikes_pattern1:
        # Pattern 2: Just look for dislikes section
        dislikes_pattern1 = re.search(r'[Dd]islikes[^:]*:?\s*(.*?)(?=\n[LlDd]|$)', content, re.DOTALL)

    if dislikes_pattern1:
        dislikes_text = dislikes_pattern1.group(1).strip()
        # Extract individual dislikes from bullet points
        dislikes_items = re.findall(r'[•\u2022]\s*([^\n\r]+)', dislikes_text)
        alter_data["affective"]["preferences"]["mild"]["dislikes"] = [item.strip().rstrip('.') for item in dislikes_items if item.strip()]

    # Extract boundaries
    dm_match = re.search(r'(?:[Dd]m|DMs|Dms|DMS|დმ|დმს)[^:]*:?\s*([^\n\r]+)', content, re.IGNORECASE)
    if dm_match:
        alter_data["relational"]["boundaries"]["dm_request"] = dm_match.group(1).strip()

    friend_req_match = re.search(r'(?:[Ff]riend\s*[Rr]eq|FRQ|friend req|Friend Req)[^:]*:?\s*([^\n\r]+)', content, re.IGNORECASE)
    if friend_req_match:
        alter_data["relational"]["boundaries"]["friend_request"] = friend_req_match.group(1).strip()

    # Extract favorite colors
    color_match = re.search(r'(?:[Cc]olor|colour|Color|Colour|Favourite|Favorite|colors|colours|[\u10e6\u10e7]\s*[Cc]olou?r[^*]*[\u10e6\u10e7])[^:]*:?\s*([^\n\r]+)', content)
    if color_match:
        colors_text = color_match.group(1).strip()
        colors = re.split(r'[/,]', colors_text)
        alter_data["world"]["affinities"]["toward"]["aesthetic"]["colors"] = [c.strip() for c in colors if c.strip()]

    return alter_data

def parse_introductions_to_json():
    """Parse all .mx files in introductions/ and save to database/alters.json"""
    introductions_dir = "introductions"
    output_file = "database/alters.json"
    
    if not os.path.exists(introductions_dir):
        print(f"Directory {introductions_dir} does not exist")
        return
    
    all_alters = []
    
    for filename in os.listdir(introductions_dir):
        if filename.endswith('.mx'):
            file_path = os.path.join(introductions_dir, filename)
            alter_data = parse_mx_file(file_path)
            all_alters.append(alter_data)
    
    # Write to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_alters, f, indent=2, ensure_ascii=False)
    
    print(f"Parsed {len(all_alters)} alters and saved to {output_file}")

if __name__ == "__main__":
    parse_introductions_to_json()