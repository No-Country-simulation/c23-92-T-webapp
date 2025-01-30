from flask import Blueprint, jsonify, request, make_response
from src.utils.Logger import Logger
from src.utils.Security import Security
from src.services.TokensService import TokensService

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