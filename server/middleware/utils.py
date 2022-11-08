import json
from bson import json_util

def validate_input(input, expectedType, field):
            
    if input is None:
        raise Exception(f"Cannot create user with no valid {field}")
    
    if isinstance(input, expectedType):
        return input
    raise AssertionError("[validate_input] Invalid input for type", field)

def parse_json(data):
    return json.loads(json_util.dumps(data))