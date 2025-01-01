import re
import json

def is_json(string):
    # Regex pattern for JSON
    json_pattern = r'^(\s*\{.*\}\s*|\s*\[.*\]\s*)$'
    
    # Check if the string matches the JSON pattern
    if re.match(json_pattern, string, re.DOTALL):
        # Additional validation using json.loads()
        try:
            json.loads(string)
            return True
        except json.JSONDecodeError:
            return False
    return False



def is_valid_json(s):
    try:
        json.loads(s)
        return True
    except ValueError:
        return False
    

def clean_json_string(input_string):
    # Remove leading and trailing whitespace
    cleaned = input_string.strip()
    
    # Remove the "```json" at the beginning and "```" at the end
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```python"):
        cleaned = cleaned[9:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    
    # Remove any remaining leading/trailing whitespace
    cleaned = cleaned.strip()
    
    return cleaned