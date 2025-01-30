from functools import wraps
from flask import request, jsonify, redirect, Response
from src.utils.Security import Security
from src.utils.Logger import Logger
import jwt
import json
import traceback

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
                token_result = Security.get_secure_cookie('token', max_age=7200)
                device_id_result = Security.get_secure_cookie('device_id', max_age=30 * 24 * 60 * 60)  # 30 days

                Logger.add_to_log("info", f"Token result: {token_result}")
                Logger.add_to_log("info", f"Device ID result: {device_id_result}")

                if not token_result.get('success') or not device_id_result.get('success'):
                    Logger.add_to_log("info", "No token or device_id provided")
                    refresh_response = Security.refresh_token_from_cookie()

                    if not isinstance(refresh_response, Response):
                        Logger.add_to_log("info", "Redirecting to login")
                        return redirect("/login")

                    return refresh_response  # Devolver la respuesta con el nuevo access_token

                access_token = token_result['value']
                device_id = device_id_result['value']

                try:
                    payload = jwt.decode(
                        access_token, 
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
                    Logger.add_to_log("info", "Token has expired")

                    refresh_response = Security.refresh_token_from_cookie()
                    return refresh_response

                except jwt.InvalidTokenError as e:
                    Logger.add_to_log("info", f"Invalid token: {str(e)}")
                    return jsonify({
                        'success': False,
                        'message': 'Invalid token',
                        'redirect': LOGIN_REDIRECT
                    }), 401

                if not Security.is_valid_payload(payload):
                    Logger.add_to_log("info", "Invalid token payload")
                    return jsonify({
                        'success': False,
                        'message': 'Invalid token payload',
                        'redirect': LOGIN_REDIRECT
                    }), 401

                # Verificar que el device_id del token coincida con el de la cookie
                if payload['device_id'] != device_id:
                    Logger.add_to_log("info", "Device ID mismatch")
                    return jsonify({
                        'success': False,
                        'message': 'Invalid device',
                        'redirect': LOGIN_REDIRECT
                    }), 401

                if not Security.validate_device(payload['id'], payload['device_id']):
                    Logger.add_to_log("info", f"Unauthorized device for user: {payload.get('id')}")
                    response = Security.clear_device_cookies()
                    response.status_code = 401
                    response.data = json.dumps({
                        'success': False,
                        'message': 'Unauthorized device',
                        'redirect': LOGIN_REDIRECT
                    })
                    return response

                Logger.add_to_log("info", f"Authenticated user: {payload.get('id')}")

                kwargs['user_id'] = payload.get('id')
                kwargs['device_id'] = payload.get('device_id')

                return f(*args, **kwargs)

            except Exception as ex:
                Logger.add_to_log("error", f"Authentication error: {str(ex)}")
                Logger.add_to_log("error", traceback.format_exc())
                return jsonify({
                    'success': False,
                    'message': 'Authentication error',
                    'redirect': LOGIN_REDIRECT
                }), 500
        return decorated
        
    @classmethod
    def reject_authenticated_json(cls, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            access_token = Security.get_secure_cookie('token', max_age=7200)  # 2 horas
            
            if access_token and access_token['success']:
                try:
                    print("Access token:", access_token)
                    result = Security.verify_token(access_token['value'])
                    if result['success']:
                        return redirect('/testSocket')
                    else:
                        print(f"Token is invalid: {result['message']}")
                
                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
                    print(f"Token error: {e}")

            return f(*args, **kwargs)
        
        return decorated_function
    
    @classmethod
    def reject_authenticated_json_server(cls, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            access_token = Security.get_secure_cookie('token', max_age=7200)  # 2 horas
            
            if access_token and access_token['success']:
                try:
                    print("Access token:", access_token)
                    result = Security.verify_token(access_token['value'])
                    if result['success']:
                        return jsonify({
                            'success': False,
                            'message': 'You are already authenticated',
                            'redirect': '/testSocket'
                        }), 403
                    else:
                        print(f"Token is invalid: {result['message']}")
                
                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
                    print(f"Token error: {e}")

            return f(*args, **kwargs)
        
        return decorated_function