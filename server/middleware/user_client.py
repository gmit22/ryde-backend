from bson import ObjectId
from flask import current_app as app
from middleware.utils import validate_input, parse_json
import datetime

user_collection_name = "users"

def add_user(user):
    user_collection = app.db[user_collection_name]
    u_id = user_collection.insert_one(user)
    return u_id.inserted_id
    
def create_new_user(user_data):
       
    try:      
        name = validate_input(user_data.get('name'), str, 'name')
        dob = validate_input(user_data.get('dob'), str, 'dob')
        address = validate_input(user_data.get('address'), str, 'address')
        description = validate_input(user_data.get('description'), str, 'description')
            
    except Exception as e:
        raise Exception(f"[parse_user] {str(e)}")
    
    if user_data.get("createdAt") is not None:
        raise Exception("[create_new_user] The creation timing of the user has to be stamped by API")     
    
    if user_data.get("friends") is not None:
        raise Exception("[create_new_user] The user cannot be created with friends as an input")  
          
    user = {
        "name": name, 
        "dob": dob, 
        "address": address,
        "description": description,
        "createdAt": datetime.datetime.now(),
    }
    
    u_id = add_user(user)
    return u_id

def get_user_by_id(id):

    # db = init_connection()
    user_collection = app.db[user_collection_name]
    user = user_collection.find_one({"_id": ObjectId(id)})
    
    return parse_json(user)

def get_all_users():
    # db = init_connection()
    user_collection = app.db[user_collection_name]
    resp = user_collection.find()
    total_users = list(resp)
    
    # if len(total_users) == 0:
    #     raise Exception(f"[get_all_users] No users were found stored in the db.")
    return parse_json(total_users)

def delete_user_by_id(id):
    
    user = get_user_by_id(id)
    if user is None:
        return None
    
    # db = init_connection()
    user_collection = app.db[user_collection_name]      
    resp = user_collection.delete_one({"_id": ObjectId(id)})
    return resp

def update_user_by_id(u_id, user_data):

    user = get_user_by_id(u_id)
    if user is None:
        return None
    
    # db = init_connection()
    user_collection = app.db[user_collection_name]
    
    name = user_data.get("name")
    dob = user_data.get("dob")
    address = user_data.get("address")
    description = user_data.get("description")
    friends = user_data.get("friends")

    changed_fields = {}
    # Add another try/catch here to backtrack to relevant function
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
            
    except AssertionError as e:
        raise AssertionError(f"[update_user_by_id] {str(e)}")
    
    update = {"$set": changed_fields}

    response = user_collection.update_one(
        {"_id": ObjectId(u_id)}, 
        update=update
    )
       
    return response

def add_friend_to_user(user_id, friend_id):
   
    if user_id == friend_id:
        raise Exception("[add_friend_to_user] user_id and friend_id must be different for the friend.")

    # Error handling in case friend is not found
    user = get_user_by_id(user_id)
    friend = get_user_by_id(friend_id)

    if user is None or friend is None:
        return None
    
    if "friends" not in user:
        user["friends"] = [friend_id]
    
    else:
        curr_friends = user["friends"]
        for curr_friend in curr_friends:
            if curr_friend == friend_id:
                raise Exception(f"[add_friend_to_user] The user {friend_id} is already a friend of the user {user_id}.")
        
        
        user["friends"].append(friend_id)

    update_status = update_user_by_id(user_id, user)
    
    return update_status