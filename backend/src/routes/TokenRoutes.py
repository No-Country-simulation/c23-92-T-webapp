import traceback
from flask import Blueprint, jsonify, request
from src.utils.Logger import Logger
from src.utils.Security import Security

token_routes = Blueprint('token_routes', __name__)

@token_routes.route('/refresh', methods=['POST'])
def refresh_token():
    try:
        result = Security.handle_token_refresh(request.json)
        if not result:
            return jsonify({'error': 'Invalid refresh token'}), 401
        return jsonify(result), 200
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500
