from functools import wraps
from flask import request, jsonify
from src.utils.Security import Security
from src.utils.Logger import Logger
import jwt

LOGIN_REDIRECT = '/login'

class AuthMiddleware:
    @staticmethod
    def validate_request_data(required_fields):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                try:
                    data = request.get_json()
                    if not data:
                        return jsonify({
                            'success': False,
                            'message': 'No data provided'
                        }), 400

                    missing_fields = [field for field in required_fields if not data.get(field)]
                    if missing_fields:
                        return jsonify({
                            'success': False,
                            'message': f'Missing required fields: {", ".join(missing_fields)}'
                        }), 400

                    return f(*args, **kwargs)
                except Exception as e:
                    Logger.error(f"Request validation failed: {str(e)}")
                    return jsonify({
                        'success': False,
                        'message': 'Invalid request format'
                    }), 400
            return decorated_function
        return decorator

    @staticmethod
    def require_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                if 'Authorization' not in request.headers:
                    return jsonify({
                        'error': 'No token provided',
                        'redirect': LOGIN_REDIRECT,
                        'status': 401,
                    }), 401

                is_valid = Security.verify_token(request.headers)
                if not is_valid:
                    return jsonify({
                        'error': 'Invalid or expired token',
                        'status': 401,
                        'redirect': LOGIN_REDIRECT
                    }), 401
                
                Logger.add_to_log("info", f"Authorization header: {request.headers['Authorization']}")

                token = request.headers['Authorization'].split(" ")[1]
                payload = jwt.decode(token, Security.secret, algorithms=["HS256"])
                kwargs['user_id'] = payload.get('id')

                return f(*args, **kwargs)
            except Exception as ex:
                Logger.add_to_log("error", str(ex))
                return jsonify({
                    'error': 'Authentication error',
                    'status': 500,
                    'redirect': LOGIN_REDIRECT
                }), 500
        return decorated

    @staticmethod
    def get_current_user():
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({
                    'error': 'No token provided',
                    'redirect': LOGIN_REDIRECT,
                    'status': 401,
                })
                
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, Security.secret, algorithms=["HS256"])
            return payload.get('id')
        except Exception:
            return jsonify({
                'error': 'Invalid token',
                'status': 401,
                'redirect': LOGIN_REDIRECT
            }), 401