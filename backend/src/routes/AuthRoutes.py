from flask import Blueprint, request, jsonify
from src.services.AuthService import AuthService
from src.repositories.UserRepository import UserRepository
from src.utils.Logger import Logger
from src.utils.Security import Security
import traceback

auth_routes = Blueprint('auth_routes', __name__)

auth_service = AuthService()

@auth_routes.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400
        
        authenticated_user = auth_service.login_user(username, password)

        if (authenticated_user != None):
            encoded_access_token, encoded_refresh_token = Security.generate_token(authenticated_user)
            return jsonify({
                'success': True,
                'access_token': encoded_access_token,
                'refresh_token': encoded_refresh_token
            }), 200
        else:
            response = jsonify({'message': 'Unauthorized'})
            return response, 401
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@auth_routes.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        timezone = data.get('timezone', 'UTC')

        response = auth_service.register_user(username, email, password, timezone)

        if 'success' in response and response['success']:
            return jsonify({'message': 'User registered successfully'}), 201
        else:
            return jsonify(response), 400

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500