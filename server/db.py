from bson import ObjectId
import pymongo
from middleware.utils import validate_input, parse_json
import datetime

connection_url = "mongodb+srv://gunit_ryde:gunit_ryde@ryde-cluster.pdveurs.mongodb.net/?retryWrites=true&w=majority"
db_name = "rydedb"
user_collection_name = "users"

def init_connection():
    client = pymongo.MongoClient(connection_url)
    db = client.get_database(db_name)    
    return db

def add_user(user):
    db = init_connection()
    user_collection = db[user_collection_name]
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

    db = init_connection()
    user_collection = db[user_collection_name]
    user = user_collection.find_one({"_id": ObjectId(id)})
    
    return parse_json(user)

def get_all_users():
    db = init_connection()
    user_collection = db[user_collection_name]
    
    resp = user_collection.find()
    total_users = list(resp)
    
    # if len(total_users) == 0:
    #     raise Exception(f"[get_all_users] No users were found stored in the db.")
    return parse_json(total_users)