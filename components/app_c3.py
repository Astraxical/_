import json
from typing import Dict, List, Any

class AlterProfile:
    """
    Class representing an alter profile based on the template structure
    """
    
    def __init__(self, name: str):
        self.data = {
            "self": {
                "name": name,
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
    
    def update_self_info(self, name: str = None, age: int = None, 
                         gender: str = None, pronouns: List[str] = None, 
                         orientation: str = None, self_perception: str = None):
        """Update self information"""
        if name is not None:
            self.data["self"]["name"] = name
        if age is not None:
            self.data["self"]["age"] = age
        if gender is not None:
            self.data["self"]["gender"] = gender
        if pronouns is not None:
            self.data["self"]["pronouns"] = pronouns
        if orientation is not None:
            self.data["self"]["orientation"] = orientation
        if self_perception is not None:
            self.data["self"]["self_perception"] = self_perception
    
    def add_like(self, like: str):
        """Add a like to mild preferences"""
        self.data["affective"]["preferences"]["mild"]["likes"].append(like)
    
    def add_dislike(self, dislike: str):
        """Add a dislike to mild preferences"""
        self.data["affective"]["preferences"]["mild"]["dislikes"].append(dislike)
    
    def add_love(self, love: str):
        """Add a love to intense preferences"""
        self.data["affective"]["preferences"]["intense"]["loves"].append(love)
    
    def add_hate(self, hate: str):
        """Add a hate to intense preferences"""
        self.data["affective"]["preferences"]["intense"]["hates"].append(hate)
    
    def add_positive_trigger(self, trigger: str):
        """Add a positive trigger"""
        self.data["affective"]["triggers"]["positive"].append(trigger)
    
    def add_negative_trigger(self, trigger: str):
        """Add a negative trigger"""
        self.data["affective"]["triggers"]["negative"].append(trigger)
    
    def get_profile(self) -> Dict[str, Any]:
        """Get the complete profile data"""
        return self.data
    
    def get_name(self) -> str:
        """Get the alter's name"""
        return self.data["self"]["name"]
    
    def get_pronouns(self) -> List[str]:
        """Get the alter's pronouns"""
        return self.data["self"]["pronouns"]