import json
from bson import json_util
from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 6378.1

""""
    Validates and ensures that the input fields are of the required/expected type.
"""
def validate_input(input, expectedType, field):
            
    if input is None and (field == "latitude" or field == "longitude"):
        return None
            
    if input is None:
        raise Exception(f"Cannot create user with no valid {field}")
    
    if isinstance(input, expectedType):
        return input
    raise AssertionError(f"[validate_input] Invalid input for field {field}")

"""
    Helps in parsing user response containing bson.ObjectId '_id' for user or list of users.
"""
def parse_json(data):
    return json.loads(json_util.dumps(data))

""""
    Helper function to compute distance between two places, given latitude and longitude for each location.
"""
def compute_distance(lat1, lon1, lat2, lon2):
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return round(distance, 3)