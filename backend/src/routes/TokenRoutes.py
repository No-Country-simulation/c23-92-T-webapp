from flask import Blueprint, jsonify, request, make_response
from src.utils.Logger import Logger
from src.utils.Security import Security
from src.services.TokensService import TokensService
import jwt

token_routes = Blueprint('token_routes', __name__)

tokens_service = TokensService()

INTERNAL_SERVER_ERROR = {'success': False, 'message': 'Internal server error'}
    
@token_routes.route('/refresh_token', methods=['POST'])
def refresh_token():
    try:
        response = Security.refresh_token_from_cookie()
        return response
    except Exception as ex:
        Logger.add_to_log("error", f"Error refreshing token: {str(ex)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500
    
@token_routes.route('/verify_token', methods=['GET'])
def verify_token():
    try:
        access_token = Security.get_secure_cookie('token', max_age=7200)  # 2 horas
        if access_token and access_token['success']:
            result = Security.verify_token(access_token['value'])
            return jsonify(result)
        else:
            return jsonify({
                'success': False,
                'message': 'No token provided'
            }), 403
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        return jsonify({
            'success': False,
            'message': f"Error verifying token: {str(ex)}"
        }), 500 