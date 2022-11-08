from flask import Blueprint, request, jsonify
from models.user import User
from db import create_new_user, get_user_by_id, get_all_users, delete_user_by_id

users_api = Blueprint(
    'users_api', 'users_api', url_prefix='/api/v1/')

@users_api.route('/user', methods=["POST"])
def create_user():

    user_data = request.get_json()
    try:
        u_id = create_new_user(user_data)
        return jsonify({"u_id": str(u_id)}), 201  
    except Exception as e:
        return jsonify({'error': f'[create_user] {str(e)}'}), 400

@users_api.route('/user/<id>', methods=["GET"])
def get_user(id):
    
    try:
        user = get_user_by_id(id)
        if user is None:
            return jsonify(f"No valid user found with matching user_id {id}"), 404
    
        return jsonify(user), 200
    
    except Exception as e:
        return jsonify(f"[get_user] {str(e)}"), 400
    
@users_api.route('/user', methods=["GET"])
def get_users():
    try:
        user_details = get_all_users()
        if user_details is None:
            user_details = []
        return jsonify({"users": user_details}), 200
        
    except Exception as e:
        return jsonify({"error": f'[get_user] {str(e)}'}), 400
    
@users_api.route('/delete-user/<id>', methods=["Post"])
def delete_user(id):
    
    try:
        delete_status = delete_user_by_id(id)
        
        # Can return 204 to depict that the non-existent client has been deleted, but 404 seems more fit since the client does not exist.
        if delete_status is None:
            return jsonify({"Status": "The requested user_id does not exist in the database"}), 404
        
        if delete_status.deleted_count == 0:
            raise Exception("The user_id could not be deleted.")
        
        return jsonify({"Status": "Success"}), 200
    
    except AssertionError as e:
        return jsonify(f"[delete_user_by_id] {str(e)}"), 400