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
                        'success': False,
                        'message': 'No token provided',
                        'redirect': LOGIN_REDIRECT,
                    }), 401
    
                auth_header = request.headers['Authorization']
                parts = auth_header.split()
                if len(parts) != 2 or parts[0].lower() != 'bearer':
                    return jsonify({
                        'success': False,
                        'message': 'Invalid authorization header format',
                        'redirect': LOGIN_REDIRECT,
                        'status': 401,
                    }), 401
    
                token = parts[1]
    
                try:
                    payload = jwt.decode(
                        token, 
                        Security.secret, 
                        algorithms=["HS256"],
                        options={
                            'verify_signature': True,
                            'require_exp': True,
                            'verify_exp': True,
                            'verify_iat': True
                        }
                    )
                except jwt.ExpiredSignatureError:
                    return jsonify({
                        'success': False,
                        'message': 'Token has expired',
                        'redirect': LOGIN_REDIRECT
                    }), 401
                except jwt.InvalidTokenError as e:
                    return jsonify({
                        'success': False,
                        'message': f'Invalid token: {str(e)}',
                        'redirect': LOGIN_REDIRECT
                    }), 401
    
                if not Security.is_valid_payload(payload):
                    return jsonify({
                        'success': False,
                        'message': 'Invalid token payload',
                        'redirect': LOGIN_REDIRECT
                    }), 401
    
                is_valid = Security.verify_token(request.headers)
                if is_valid['success'] == False:
                    return jsonify({
                        'success': False,
                        'message': 'Token validation failed',
                        'redirect': LOGIN_REDIRECT
                    }), 401
                
                if not Security.validate_device(payload['id'], payload['device_id']):
                    return jsonify({
                        'success': False,
                        'message': 'Unauthorized device',
                        'redirect': LOGIN_REDIRECT
                    }), 401
    
                Logger.add_to_log("info", f"Authenticated user: {payload.get('id')}")
    
                kwargs['user_id'] = payload.get('id')
                kwargs['device_id'] = payload.get('device_id')
    
                return f(*args, **kwargs)
    
            except Exception as ex:
                # Logging de errores inesperados
                Logger.add_to_log("error", f"Authentication error: {str(ex)}")
                return jsonify({
                    'success': False,
                    'message': f'Unexpected authentication error: {str(ex)}',
                    'redirect': LOGIN_REDIRECT
                }), 500
        return decorated

    @staticmethod
    def get_current_user():
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({
                    'success': False,
                    'message': 'No token provided',
                    'redirect': LOGIN_REDIRECT,
                }), 401
                
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, Security.secret, algorithms=["HS256"])
            return payload.get('id')
        except Exception as ex:
            return jsonify({
                'success': False,
                'message': f"Error getting current user: {str(ex)}",
                'redirect': LOGIN_REDIRECT
            }), 500