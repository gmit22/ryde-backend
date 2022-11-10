from flask import Blueprint, request, jsonify
from middleware.user_client import create_new_user, get_user_by_id, get_all_users, delete_user_by_id, update_user_by_id, \
    add_friend_to_user, get_nearby_users
from flask import request, jsonify

# imports for PyJWT authentication
import jwt
from functools import wraps

users_api = Blueprint(
    'users_api', 'users_api', url_prefix='/api/v1/')

#secret key used for encoding data
SECRET_KEY="hashencodetoken"
#encryption algorithm
ALGORITHM = "HS256"

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({"error": "The given token has an invalid signature"}) , 401
        except Exception as e:
            return jsonify({
                'message' : f'{str(e)}'
            }), 401
  
        return  f(*args, **kwargs)
  
    return decorated

@users_api.route('/user', methods=["POST"])
@token_required
def create_user():

    user_data = request.get_json()
    try:
        u_id = create_new_user(user_data)
        return jsonify({"u_id": str(u_id)}), 201  
    except Exception as e:
        return jsonify({'error': f'[create_user] {str(e)}'}), 400

@users_api.route('/user/<id>', methods=["GET"])
@token_required
def get_user(id):
    
    try:
        user = get_user_by_id(id)
        if user is None:
            return jsonify(f"No valid user found with matching user_id {id}"), 404
    
        return jsonify(user), 200
    
    except Exception as e:
        return jsonify(f"[get_user] {str(e)}"), 400
    
@users_api.route('/users', methods=["GET"])
@token_required
def get_users():
    try:
        user_details = get_all_users()
        if user_details is None:
            user_details = []
        return jsonify({"users": user_details}), 200
        
    except Exception as e:
        return jsonify({"error": f'[get_user] {str(e)}'}), 400
    
@users_api.route('/delete-user/<id>', methods=["Post"])
@token_required
def delete_user(id):
    
    try:
        delete_resp = delete_user_by_id(id)
        
        # Can return 204 to depict that the non-existent client has been deleted, but 404 seems more fit since the client does not exist.
        if delete_resp is None:
            return jsonify({"Status": "The requested user_id does not exist in the database"}), 404
        
        if delete_resp.deleted_count == 0:
            raise Exception("The user_id could not be deleted.")
        
        return jsonify({"Status": "Success"}), 200
    
    except AssertionError as e:
        return jsonify(f"[delete_user_by_id] {str(e)}"), 400
    
@users_api.route('/update-user/<id>', methods=["Put"])
@token_required
def update_user(id):

    user_data = request.args
    try:         
       
        upsert_resp = update_user_by_id(id, user_data)
        # We do not permit creating elements via the PUT method.
        if upsert_resp is None:
            return jsonify({"Status": "The requested user_id does not exist in the database"}), 404
        
        if upsert_resp.modified_count == 0:
            raise Exception("The user_id could not be updated.")
        
        return jsonify({"Status": "Success"}), 200
    
    except AssertionError as e:
        return jsonify({"error": f"[update_user] Input type mismatch {str(e)}"})
    
    except Exception as e:
        return jsonify({"error": f"[update_user] {str(e)} "}), 400

@users_api.route('/add-friend', methods=['Put'])
@token_required
def add_friend():
    
    user_id = request.args.get('userId')
    friend_id = request.args.get('friendId')

    try:
        if user_id is None or friend_id is None:
            raise Exception("We need the user_id and the friend_id to perform the required operation.")
        
        friend_user_update = add_friend_to_user(user_id, friend_id)
        user_friend_update = add_friend_to_user(friend_id, user_id)
        
        if friend_user_update is None or user_friend_update is None:
            return jsonify({"Status": "The requested user_id or friend_id does not exist in the database"}), 404 
            
        return jsonify({"status": f"Success"}), 200
        
    except Exception as e:
        return jsonify({"error": f"{str(e)}"}), 400
  
@users_api.route('/get-nearby-friends/<id>', methods=['Get'])  
@token_required
def get_nearby_friends(id):
    
    limit = request.args.get('limit')
    max_distance = request.args.get('distance')
    
    try:
        nearby_friends = get_nearby_users(id, max_distance, limit)
        
        if nearby_friends is None:
            return jsonify({"Status": "The requested user_id does not exist in the database"}), 404
        if nearby_friends == []:
            return jsonify({"Status": "No friends exist for the user satisfying the given criteria"}), 200

        return jsonify({"users": nearby_friends}), 200
        
    except Exception as e:
        return jsonify(f"[get_nearby_friends] {str(e)}"), 400
        