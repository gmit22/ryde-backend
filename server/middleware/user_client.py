from bson import ObjectId
from flask import current_app as app
from middleware.utils import validate_input, parse_json, compute_distance
import datetime

user_collection_name = "users"

def add_user(user: dict):
    user_collection = app.db[user_collection_name]
    u_id = user_collection.insert_one(user)
    return u_id.inserted_id if u_id else None

"""
    Parses the given input to check and validate each field of the user data against the expected types. 
    Ensures that the user does not provide friends or createdAt; as this is added through the API only.
"""
def create_new_user(user_data: dict):
       
    try:      
        name = validate_input(user_data.get('name'), str, 'name')
        dob = validate_input(user_data.get('dob'), str, 'dob')
        address = validate_input(user_data.get('address'), str, 'address')
        description = validate_input(user_data.get('description'), str, 'description')
        longitude = validate_input(user_data.get('longitude'), float, 'longitude')
        latitude = validate_input(user_data.get('latitude'), float, 'latitude')
            
    except Exception as e:
        app.logger.error(f"{str(e)}")
        raise Exception(f"[parse_user] {str(e)}")
    
    if user_data.get("createdAt") is not None:
        app.logger.error("[create_new_user] The creation timing of the user has to be stamped by API")
        raise Exception("The creation timing of the user has to be stamped by API")     
    
    if user_data.get("friends") is not None:
        app.logger.error("[create_new_user] The user cannot be created with friends as an input")
        raise Exception("The user cannot be created with friends as an input")  
          
    user = {
        "name": name, 
        "dob": dob, 
        "address": address,
        "description": description,
        "createdAt": datetime.datetime.now(),
        "longitude": longitude,
        "latitude": latitude
    }
    
    u_id = add_user(user)
    app.logger.info(f"[create_new_user] {user} added to the database, with u_id to the database {u_id}")
    return u_id

def get_user_by_id(id: str):
    user_collection = app.db[user_collection_name]
    user = user_collection.find_one({"_id": ObjectId(id)})
    app.logger.info(f"[get_user_by_id] {user} corresponding to {id} found in the database")
    return parse_json(user)

def get_all_users():
    user_collection = app.db[user_collection_name]
    resp = user_collection.find()
    total_users = list(resp)
    app.logger.info(f"[get_all_users] Total {len(total_users)} users found in the database")
    return parse_json(total_users)

"""
    Check if the user to be deleted exists in the db, if they exist then delete from the db else return None.     
"""
def delete_user_by_id(id: str):
    
    user = get_user_by_id(id)
    if user is None:
        app.logger.warning(f"[delete_user_by_id] No user corresponding to {id} found in the database")
        return None
    
    user_collection = app.db[user_collection_name]      
    resp = user_collection.delete_one({"_id": ObjectId(id)})
    return resp

"""
    Given the user_data, and u_id for the corresponding user; extract the fields provided to make an update to the 
    user entity.
"""
def update_user_by_id(u_id: str, user_data: dict):

    user = get_user_by_id(u_id)
    if user is None:
        app.logger.warning(f"[update_user_by_id] No user corresponding to {u_id} found in the database")
        return None
    
    user_collection = app.db[user_collection_name]
    
    name = user_data.get("name")
    dob = user_data.get("dob")
    address = user_data.get("address")
    description = user_data.get("description")
    friends = user_data.get("friends")
    latitude = user_data.get("latitude")
    longitude = user_data.get("longitude")

    changed_fields = {}
    # Add another try/catch here to backtrack to relevant function
    # Sets the value for the updated fields, while validating the input provided by the user.
    try:
        if name is not None:
            changed_fields['name'] = validate_input(name, str, 'name')
        if dob is not None:
            changed_fields['dob'] = validate_input(dob, str, 'dob')
        if address is not None:
            changed_fields['address'] = validate_input(address, str, 'address')
        if description is not None:
            changed_fields['description'] = validate_input(description, str, 'description')
        if friends is not None:
            changed_fields["friends"] = friends
        if latitude is not None:
            changed_fields["latitude"] = latitude
        if longitude is not None:
            changed_fields["longitude"] = longitude
            
    except AssertionError as e:
        app.logger.error(f"[updated_user_by_id] {str(e)}")
        raise AssertionError(f"{str(e)}")
    
    update = {"$set": changed_fields}

    response = user_collection.update_one(
        {"_id": ObjectId(u_id)}, 
        update=update
    )
       
    return response

"""
    Adds a friend to the user, and ensures that the user is not trying to add themselves as a friend.  
    Keeps check that the same user is not added as a friend if they already exist in the friends.
"""
def add_friend_to_user(user_id: str, friend_id: str):
   
    if user_id == friend_id:
        app.logger.error(f"[add_friend_to_user] user cannot add themself as a friend. user_id and friend_id must be different")
        raise Exception("user_id and friend_id must be different for the friend.")

    # Checks that a user corresponding to the provided user_id, friend_id exists in the database.
    user = get_user_by_id(user_id)
    friend = get_user_by_id(friend_id)

    if user is None or friend is None:
        return None
    
    if "friends" not in user:
        app.logger.info(f"[add_friend_to_user] No friends currently exist associated to {user_id}")
        user["friends"] = [friend_id]
    else:
        curr_friends = user["friends"]
        for curr_friend in curr_friends:
            if curr_friend == friend_id:
                app.logger.error(f"[add_friend_to_user] {friend_id} is already a friend of user {user_id}")
                raise Exception(f"The user {friend_id} is already a friend of the user {user_id}.")
        
        user["friends"].append(friend_id)

    update_status = update_user_by_id(user_id, user) 
    return update_status

"""
    Gets friends for a user, which are in a certain proximity as specified. We ensure that the user, and friends exist in 
    the db and have a valid longitude/latitude specified. 
    In case no limit is specified, we return all the people found.
"""

def get_nearby_users(user_id: str, distance: str, limit=None):
    
    user = get_user_by_id(user_id)
    # In case no user associated to user_id found, we return None
    if user is None:
        return None
    
    if limit is not None:
        max_users = int(limit)

    if (user.get("longitude") is None and user.get("latitude") is None):
        app.logger.error(f"[get_nearby_users] user does not have both latitude and longitude values")
        raise Exception("user does not have both latitude and longitude values")
       
    longitude = float(user.get("longitude"))
    latitude = float(user.get("latitude"))
    
    dist = float(distance)    
    number_of_friends = 0
    nearby_friends = []
    
    if user.get("friends") is None or len(user["friends"]) == 0:
        app.logger.error(f"[get_nearby_users] No friends associated to the given user {user_id} found")
        return nearby_friends
    else:
        total_friends = user.get("friends")
        
        for friend_id in total_friends:
            # In case limit is not specified, we return all the users satisfying the given criteria.
            # If the required number of friends are found, we return the found friends.
            if limit is not None and number_of_friends >= max_users:
                break
            friend = get_user_by_id(friend_id)
            
            # Check to ensure that user exists and has latitude/longitude values.
            if friend and not(friend.get("longitude") is None and friend.get("latitude") is None):
               
                friend_longitude = float(friend["longitude"])
                friend_latitude = float(friend["latitude"])  
                curr_dist = compute_distance(lat1=latitude, lat2=friend_latitude, lon1=longitude, lon2=friend_longitude)

                if curr_dist <= dist:
                    nearby_friends.append(friend)
                    number_of_friends += 1 
        
    app.logger.info(f"[get_nearby_users] Total {len(nearby_friends)} found associated to the given user")
    return nearby_friends
