import json
import os
from typing import List, Dict, Any

class JSONStorage:
    """Handles JSON file operations for data persistence"""
    
    def __init__(self, filepath):
        self.filepath = filepath
    
    def load(self) -> List[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r') as f:
                    return json.load(f)
            return []
        except json.JSONDecodeError:
            print(f"Warning: {self.filepath} is corrupted. Starting with empty data.")
            return []
        except Exception as e:
            print(f"Error loading {self.filepath}: {e}")
            return []
    
    def save(self, data: List[Dict[str, Any]]) -> bool:
        """Save data to JSON file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving to {self.filepath}: {e}")
            return False