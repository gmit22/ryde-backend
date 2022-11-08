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
        raise Exception("[parse_user] The creation timing of the user has to be stamped by API")       
          
    user = {
        "name": name, 
        "dob": dob, 
        "address": address,
        "description": description,
        "createdAt": datetime.datetime.now()
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

def update_user_by_id(u_id, request):
    
    user = get_user_by_id(id)
    if user is None:
        return None
    
    # db = init_connection()
    user_collection = app.db[user_collection_name]
    
    name = request.get("name")
    dob = request.get("dob")
    address = request.get("address")
    description = request.get("description")

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
            
    except AssertionError as e:
        raise AssertionError(f"[update_user_by_id] {str(e)}")
    
    update = {"$set": changed_fields}

    response = user_collection.update_one(
        {"_id": ObjectId(u_id)}, 
        update=update
    )
       
    return response