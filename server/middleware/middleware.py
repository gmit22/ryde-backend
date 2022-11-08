from flask import Blueprint, request, jsonify
from models.user import User
from db import create_new_user

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
    