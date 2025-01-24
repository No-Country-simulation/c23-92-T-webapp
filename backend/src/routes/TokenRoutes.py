import traceback
from flask import Blueprint, jsonify, request
from src.utils.Logger import Logger
from src.utils.Security import Security
from src.services.TokensService import TokensService

token_routes = Blueprint('token_routes', __name__)

tokens_service = TokensService()

INTERNAL_SERVER_ERROR = {'success': False, 'message': 'Internal server error'}

@token_routes.route('/refresh', methods=['POST'])
def refresh_token():
    try:
        result = Security.handle_token_refresh(request.json)
        if result['success'] == False:
            return jsonify(result), 401
        
        return jsonify(result), 200
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify(INTERNAL_SERVER_ERROR), 500
    
@token_routes.route('/device-id')
def get_device_id():
    try:
        device_id = Security.generate_device_id()
        if not device_id:
            return jsonify({'success': False, 'message': 'Device id not generated'}), 500
        return jsonify({'success': True, 'device_id': device_id}), 200
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify(INTERNAL_SERVER_ERROR), 500
    
@token_routes.route('/get-token-by-user', methods=['POST'])
def get_token_by_username():
    try:
        data = request.get_json()
        username = data.get('username')
        
        if not username:
            return jsonify({'success': False, 'message': 'Username not found'}), 400
        
        result = tokens_service.get_all_tokens_by_username(username)

        if result['success'] == False:
            return jsonify(result), 401
        
        return jsonify(result), 200
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify(INTERNAL_SERVER_ERROR), 500
