from flask import Blueprint, request, jsonify, make_response, Response
from src.services.AuthService import AuthService
from src.services.UserService import UserService
from src.utils.Logger import Logger
from src.utils.Security import Security
import traceback
from src.middlewares.AuthMiddleware import AuthMiddleware

auth_routes = Blueprint('auth_routes', __name__)

auth_service = AuthService()
user_service = UserService()

@auth_routes.route('/login', methods=['POST'])
def login():
    try:
        print("Login route")
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400

        username = data.get('username')
        password = data.get('password')
        existing_device_id = request.cookies.get('device_id') # Get device_id from cookies

        if not username or not password:
            Logger.add_to_log("error", "Username and password are required")
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400
        
        authenticated_user = auth_service.login_user(username, password)

        if isinstance(authenticated_user, dict) and 'success' in authenticated_user and authenticated_user['success'] == False:
            Logger.add_to_log("error", authenticated_user['message'])
            return jsonify(authenticated_user), 400    
        
        result = Security.generate_token(authenticated_user, existing_device_id)
        
        if not isinstance(result, Response):
            return jsonify(result), 500

        return result
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@auth_routes.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400

        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        timezone = data.get('timezone', 'UTC')

        response = auth_service.register_user(username, email, password, timezone)

        if 'success' in response and response['success']:
            return jsonify(response), 201
        else:
            return jsonify(response), 400

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'success': False, 'message': "Internal server error"}), 500
    
@auth_routes.route('/logout', methods=['POST'])
@AuthMiddleware.require_auth
def logout(user_id, device_id):
    try:
        response = auth_service.logout_user(user_id, device_id)

        response = make_response(jsonify(response), 200)

        return response
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({
            'success': False,
            'message': 'Logout failed'
        }), 500
    
@auth_routes.route('/update-password', methods=['PUT'])
@AuthMiddleware.require_auth
def update_password(user_id, device_id):
    try:
        data = request.get_json()
        Logger.add_to_log("info", f"Received data: {data}")  # Log de depuración

        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400

        current_password = data.get('current_password')
        new_password = data.get('new_password')

        Logger.add_to_log("info", f"Current password received: {current_password}")  # Log de depuración
        Logger.add_to_log("info", f"New password received: {new_password}")  # Log de depuración

        if not current_password or not new_password:
            return jsonify({'success': False, 'message': 'Both current_password and new_password are required'}), 400

        response = auth_service.change_password(user_id, current_password, new_password)
        if 'success' in response and response['success']:
            return jsonify(response), 200
        else:
            return jsonify(response), 400

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'success': False, 'message': "Internal server error"}), 500
    
@auth_routes.route('/get-user', methods=['GET'])
@AuthMiddleware.require_auth
def get_user(user_id, device_id):
    try:
        user = auth_service.get_profile(user_id)

        if 'success' in user and user['success']:
            return jsonify(user), 200
        else:
            return jsonify(user), 400

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'success': False, 'message': "Internal server error"}), 500
    
@auth_routes.route('/update-profile', methods=['PUT'])
@AuthMiddleware.require_auth
def update_profile(user_id, device_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400

        username = data.get('username')
        email = data.get('email')
        timezone = data.get('timezone')

        if not username and not email and not timezone:
            return jsonify({'success': False, 'message': 'No data provided, username, email or timezone not provided'}), 400

        response = auth_service.update_profile(user_id, device_id, username, email, timezone)

        if 'success' in response and response['success']:
            return jsonify(response), 200
        else:
            return jsonify(response), 400

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'success': False, 'message': "Internal server error"}), 500
    
@auth_routes.route('/delete-account', methods=['DELETE'])
@AuthMiddleware.require_auth
def delete_account(user_id, device_id):
    try:
        response = user_service.delete_account(user_id)

        if 'success' in response and response['success']:
            return jsonify(response), 200
        else:
            return jsonify(response), 400

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'success': False, 'message': "Internal server error"}), 500