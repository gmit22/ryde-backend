from bson import ObjectId, json_util
import pymongo
import json
from middleware.utils import validate_input
import datetime

connection_url = "mongodb+srv://gunit_ryde:gunit_ryde@ryde-cluster.pdveurs.mongodb.net/?retryWrites=true&w=majority"
db_name = "rydedb"
user_collection_name = "users"


def init_connection():
    
    client = pymongo.MongoClient(connection_url)
    db = client.get_database(db_name)    
    return db
db = init_connection()
user_collection = db[user_collection_name]

def add_user(user):
    u_id = user_collection.insert_one(user)
    print(u_id)
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
    
    print(user)
    u_id = add_user(user)
    return u_id
