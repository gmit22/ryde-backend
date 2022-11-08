from flask import Blueprint, request, jsonify
from models.user import User
from db import create_new_user, get_user_by_id

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