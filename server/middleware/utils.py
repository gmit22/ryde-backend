import json
from bson import json_util

def validate_input(input, expectedType, field):
            
    if input is None and (field == "latitude" or field == "longitude"):
        input = 0.0
            
    if input is None:
        raise Exception(f"Cannot create user with no valid {field}")
    
    if isinstance(input, expectedType):
        return input
    raise AssertionError(f"[validate_input] Invalid input for field {field}")

def parse_json(data):
    return json.loads(json_util.dumps(data))