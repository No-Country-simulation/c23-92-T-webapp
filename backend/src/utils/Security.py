import os
from dotenv import load_dotenv
import datetime
import jwt
import pytz
import traceback
from src.services.TokensService import TokensService
from itsdangerous import URLSafeTimedSerializer
from cryptography.fernet import Fernet
from flask import make_response, jsonify, request, current_app
import hashlib
import uuid

# Logger
from src.utils.Logger import Logger

load_dotenv()

REFRESH_TOKEN_HAS_EXPIRED='Refresh token has expired.'
REFRESH_TOKEN_INVALID_SIGNATURE='Invalid refresh token signature.'
INTERNAL_SERVER_ERROR='Internal server error'
INVALID_STRUCTURE='Invalid token payload structure.'
GLOBAL_ERROR='Error: '
INVALID_PAYLOAD="Invalid refresh token payload structure."
ERROR_DECRYPTING_REFRESH_TOKEN="Error decrypting refresh token."

class Security():

    tokens_service = TokensService()

    refresh_encryption_key = os.getenv("REFRESH_ENCRYPTION_KEY")
    cipher_suite = Fernet(refresh_encryption_key)
    secret = os.getenv("SECRET_KEY")
    refresh_secret = os.getenv("REFRESH_SECRET_KEY")
    cookie_secret = os.getenv("COOKIE_SECRET_KEY")
    serializer = URLSafeTimedSerializer(cookie_secret)
    default_tz = pytz.timezone("America/New_York") # Default timezone
    tz = default_tz
    MAX_DEVICES = 5

    @classmethod
    def sign_cookie(cls, data):
        return cls.serializer.dumps(data)
    
    @classmethod
    def unsign_cookie(cls, signed_data, max_age=None):
        try:
            if not signed_data or not isinstance(signed_data, str):
                Logger.add_to_log("error", "Invalid cookie value")
                return {
                    'success': False,
                    'message': 'Invalid cookie value'
                }

            result = cls.serializer.loads(signed_data, max_age=max_age)

            return {
                'success': True,
                'value': result
            }
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {
                'success': False,
                'message': f"Error unsigning cookie: {str(ex)}"
            }
    
    @classmethod
    def set_secure_cookie(cls, response, name, value, max_age=None):
        signed_value = cls.sign_cookie(value)
        response.set_cookie(
            name,
            value=signed_value,
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=max_age
        )

    @classmethod
    def get_secure_cookie(cls, name, max_age=None):
        signed_value = request.cookies.get(name)
        if not signed_value:
            Logger.add_to_log("info", f"Cookie {name} not found")
            return {
                'success': False,
                'message': f"Cookie {name} not found"
            }
        return cls.unsign_cookie(signed_value, max_age=max_age)

    @classmethod
    def get_websocket_cookie(cls, name, max_age=None):
            signed_value = request.cookies.get(name)
            if not signed_value:
                Logger.add_to_log("info", f"Cookie {name} no encontrada en WebSocket")
                return {
                    'success': False,
                    'message': f"Cookie {name} no encontrada"
                }
            return cls.unsign_cookie(signed_value, max_age=max_age)
        
    @classmethod
    def generate_device_id(cls):
        device_id = str(uuid.uuid4())

        if not device_id:
            Logger.add_to_log("error", "Device ID not generated.")
            return {
                'success': False,
                'message': 'Device ID not generated'
            }
        
        response = make_response(jsonify({
            'success': True,
            'message': 'Device ID generated successfully',
        }))

        response.set_cookie(
            'device_id',
            value=device_id,
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=30 * 24 * 60 * 60 # 30 days
        )

        return response
    
    @classmethod
    def check_device_limit(cls, user_id):
        if not user_id:
            Logger.add_to_log("error", "User ID missing.")
            return {
                'success': False,
                'message': 'User ID missing'
            }
        
        active_devices = cls.tokens_service.count_active_devices_by_user(user_id)

        if active_devices >= cls.MAX_DEVICES:
            Logger.add_to_log("warning", f"User {user_id} has reached maximum device limit ({cls.MAX_DEVICES})")

            remove = cls.remove_oldest_device(user_id)
            if not remove['success']:
                return {
                    'success': False,
                    'message': 'Device limit reached and error removing oldest device'
                }
            Logger.add_to_log("info", f"Oldest device removed for user: {user_id}")
            return {
                'success': True,
                'message': 'Oldest device remove to make space for new device'
            }
        return {
            'success': True,
            'message': 'Device limit not reached'
        }

    @classmethod
    def remove_oldest_device(cls, user_id):
        try:
            oldest_token = cls.tokens_service.get_oldest_active_token(user_id)

            if not oldest_token:
                Logger.add_to_log("error", f"No active tokens found for user: {user_id}")
                return {
                    'success': False,
                    'message': 'No active tokens found'
                }
            
            success = cls.tokens_service.revoke_token(oldest_token.id)
            if not success:
                Logger.add_to_log("error", f"Error revoking oldest token for user: {user_id}")
                return {
                    'success': False,
                    'message': 'Error revoking oldest token'
                }
            
            Logger.add_to_log("info", f"Oldest token revoked for user: {user_id}")
            return {
                'success': True,
                'message': 'Oldest token revoked'
            }
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {
                'success': False,
                'message': f"Error removing oldest device: {str(ex)}"
            }
        
    @classmethod
    def is_device_active(cls, user_id, device_id):
        try:
            active_token = cls.tokens_service.find_active_token_by_user_and_device(user_id, device_id)
            return active_token is not None
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return False

    @classmethod
    def clear_device_cookies(cls):
        response = make_response(jsonify({
            'success': True,
            'message': 'Device cookies cleared',
            'action': 'REFRESH_DEVICE_ID'
        }))
        
        response.delete_cookie('device_id')
        response.delete_cookie('token')
        response.delete_cookie('refresh_token')
        
        return response

    @classmethod
    def generate_token(cls, authenticated_user, existing_device_id=None):
        try:
            if not authenticated_user:
                Logger.add_to_log("error", "User not found.")
                return {
                    'success': False,
                    'message': 'User not found'
                }

            if existing_device_id:
                active_token = cls.tokens_service.find_active_token_by_user_and_device(
                    authenticated_user.id, 
                    existing_device_id
                )
            
                if active_token:
                    device_id = existing_device_id
                    success = cls.tokens_service.revoke_old_tokens_for_device(
                        authenticated_user.id, 
                        device_id
                    )
                    if not success:
                        Logger.add_to_log("error", "Error revoking old tokens for device.")
                        return {
                            'success': False,
                            'message': 'Error revoking old tokens for device'
                        }
                else:
                    device_id = str(uuid.uuid4())
            else:
                device_id = str(uuid.uuid4())
                
            if cls.check_device_limit(authenticated_user.id)['success'] == False:
                Logger.add_to_log("error", "Device limit reached.")
                return {
                    'success': False,
                    'message': 'Device limit reached'
                }
            
            try:
                Logger.add_to_log("info", f"User timezone: {authenticated_user.timezone}")
                cls.tz = pytz.timezone(authenticated_user.timezone)
            except Exception as ex:
                cls.tz = cls.default_tz
                Logger.add_to_log("error", str(ex))
                Logger.add_to_log("error", f"Invalid user timezone: {authenticated_user.timezone}. Using default timezone.")
                Logger.add_to_log("error", str(ex))

            Logger.add_to_log("info", f"Using timezone: {cls.tz.zone} for user {authenticated_user.username}")

            now = datetime.datetime.now(tz=cls.tz)

            payload = {
                'iat': now,
                'exp': now + datetime.timedelta(hours=2),
                'id': str(authenticated_user.id),
                'username': authenticated_user.username,
                'timezone': cls.tz.zone,
                'device_id': device_id
            }

            Logger.add_to_log("info", f"Generating token with timezone: {cls.tz.zone}")

            access_token = jwt.encode(payload, cls.secret, algorithm="HS256")

            refresh_payload = {
                'iat': now,
                'exp': now + datetime.timedelta(days=30),
                'id': str(authenticated_user.id),
                'username': authenticated_user.username,
                'timezone': cls.tz.zone,
                'device_id': device_id
            }

            Logger.add_to_log("info", f"Generating refresh token with timezone: {cls.tz.zone}")
            Logger.add_to_log("info", f"Refresh token expires at: {refresh_payload['exp']}")

            refresh_token = jwt.encode(refresh_payload, cls.refresh_secret, algorithm="HS256")

            token_signature = hashlib.sha256(refresh_token.encode()).hexdigest()

            cls.tokens_service.create_token(
                user_id=authenticated_user.id,
                token_signature=token_signature,
                refresh_token=cls.cipher_suite.encrypt(refresh_token.encode()).decode(),
                expires_at=refresh_payload['exp'],
                device_id=refresh_payload['device_id']
            )

            response = make_response(jsonify({
                'success': True,
                'message': 'Token generated successfully',
            }), 200)

            cls.set_secure_cookie(response=response, name='device_id', value=device_id, max_age=30 * 24 * 60 * 60) # 30 days
            cls.set_secure_cookie(response=response, name='token', value=access_token, max_age=7200) # 2 hours
            cls.set_secure_cookie(response=response, name='refresh_token', value=refresh_token, max_age=30 * 24 * 60 * 60) # 30 days
            
            return response
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {
                'success': False,
                'message': f"Error generating tokens: {str(ex)}"
            }

    @classmethod
    def verify_token(cls, token):
        try:
            if not token:
                Logger.add_to_log("info", "Unauthorized access: No token provided")
                return {
                    'success': False,
                    'message': 'No token provided'
                }

            if not cls.is_valid_token_format(token):
                return {
                    'success': False,
                    'message': 'Invalid token format'
                }

            try:
                payload = jwt.decode(
                    token, 
                    cls.secret, 
                    algorithms=["HS256"],
                    options={
                        'verify_signature': True,
                        'require_exp': True,
                        'verify_exp': True,
                        'verify_iat': True
                    }
                )
            except jwt.ExpiredSignatureError:
                Logger.add_to_log("error", "Token has expired")
                return {
                    'success': False,
                    'message': 'Token has expired'
                }
            except jwt.InvalidTokenError as e:
                Logger.add_to_log("error", f"Invalid token: {str(e)}")
                return {
                    'success': False,
                    'message': 'Invalid token'
                }

            if not cls.is_valid_payload(payload):
                Logger.add_to_log("error", "Invalid payload structure")
                return {
                    'success': False,
                    'message': 'Invalid payload structure'
                }
            
            refresh_token_of_user = cls.tokens_service.find_active_token_by_user_and_device(payload['id'], payload['device_id'])
            if not refresh_token_of_user:
                Logger.add_to_log("error", "No refresh token found for user and device")
                return {
                    'success': False,
                    'message': 'No refresh token found for user and device'
                }
            
            decrypted_token = cls.decrypt_refresh_token(refresh_token_of_user.refresh_token)

            if not decrypted_token:
                Logger.add_to_log("error", ERROR_DECRYPTING_REFRESH_TOKEN)
                return {
                    'success': False,
                    'message': ERROR_DECRYPTING_REFRESH_TOKEN
                }
            try:
                refresh_payload = jwt.decode(decrypted_token, cls.refresh_secret, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                Logger.add_to_log("error", REFRESH_TOKEN_HAS_EXPIRED)
                return {
                    'success': False,
                    'message': REFRESH_TOKEN_HAS_EXPIRED
                }
            except jwt.InvalidSignatureError:
                Logger.add_to_log("error", REFRESH_TOKEN_INVALID_SIGNATURE)
                return {
                    'success': False,
                    'message': REFRESH_TOKEN_INVALID_SIGNATURE
                }
            
            if not cls.is_valid_payload(refresh_payload):
                Logger.add_to_log("error", INVALID_PAYLOAD)
                return {
                    'success': False,
                    'message': INVALID_PAYLOAD
                }
            
            if refresh_payload['id'] != payload['id']:
                Logger.add_to_log("error", "User ID mismatch")
                return {
                    'success': False,
                    'message': 'User ID mismatch'
                }
            
            if refresh_payload['device_id'] != payload['device_id']:
                Logger.add_to_log("error", "Device ID mismatch")
                return {
                    'success': False,
                    'message': 'Device ID mismatch'
                }
                
            return {
                'success': True,
                'message': 'Token verified'
            }
        except Exception as ex:
            Logger.add_to_log("error", f"Unexpected token verification error: {str(ex)}")
            return {
                'success': False,
                'message': f"Unexpected error: {str(ex)}"
            }

    # Verificar si el formato del token al cumple con el formato
    @classmethod
    def is_valid_token_format(cls, token):
        Logger.add_to_log("info", f"Token in token format function: {token}")
        return len(token) > 0 and token.count('.') == 2

    # Decodificar el access token
    @classmethod
    def decode_token(cls, token):
        try:
            return jwt.decode(token, cls.secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            Logger.add_to_log("error", "Token has expired.")
            return {
                'success': False,
                'message': 'Token has expired'
            }
        except jwt.InvalidSignatureError:
            Logger.add_to_log("info", token)
            Logger.add_to_log("error", "Invalid token signature.")
            return {
                'success': False,
                'message': 'Invalid token signature'
            }
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {
                'success': False,
                'message': f"Unexpected error: {str(ex)}"
            }
    
    # Verficar si el payload del token es valido
    @classmethod
    def is_valid_payload(cls, payload):
        required_keys = ['id', 'username', 'timezone', 'device_id']
        return all(key in payload for key in required_keys)
    
    # Verificar si el refresh token del usuario es valido
    @classmethod
    def has_a_valid_refresh_token(cls, user_id, device_id):
        try:
            last_refresh_token = cls.tokens_service.find_active_token_by_user_and_device(user_id, device_id)
            if not last_refresh_token:
                Logger.add_to_log("error", "No refresh token found.")
                return {
                    'success': False,
                    'message': 'No refresh token found'
                }
            
            decrypted_token = cls.decrypt_refresh_token(last_refresh_token)
            if not decrypted_token:
                Logger.add_to_log("error", ERROR_DECRYPTING_REFRESH_TOKEN)
                return {
                    'success': False,
                    'message': ERROR_DECRYPTING_REFRESH_TOKEN
                }
            
            try:
                payload = jwt.decode(decrypted_token, cls.refresh_secret, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                Logger.add_to_log("error", REFRESH_TOKEN_HAS_EXPIRED)
                return {
                    'success': False,
                    'message': REFRESH_TOKEN_HAS_EXPIRED
                }
            except jwt.InvalidSignatureError:
                Logger.add_to_log("error", REFRESH_TOKEN_INVALID_SIGNATURE)
                return {
                    'success': False,
                    'message': REFRESH_TOKEN_INVALID_SIGNATURE
                }
            
            required_keys = ['id', 'username', 'timezone', 'device_id']
            if not all(key in payload for key in required_keys):
                Logger.add_to_log("error", INVALID_PAYLOAD)
                return {
                    'success': False,
                    'message': INVALID_PAYLOAD
                }
            
            return {
                'success': True,
                'message': 'Valid refresh token'
            }
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return False, GLOBAL_ERROR + str(ex)

    @classmethod
    def verify_refresh_token(cls, refresh_token: str):
        try:
            unverified_payload = jwt.decode(
                refresh_token,
                cls.refresh_secret,
                algorithms=["HS256"],
                options={"verify-exp": False}
            )

            stored_token = cls.tokens_service.find_active_token_by_user_and_device(unverified_payload['id'], unverified_payload['device_id'])
            if not stored_token:
                Logger.add_to_log("error", "No refresh token found for user and device credentials.")
                return {
                    'success': False,
                    'message': 'No refresh token found for user and device credentials.'
                }

            decrypted_stored_token = cls.decrypt_refresh_token(stored_token.refresh_token)
            if not decrypted_stored_token:
                Logger.add_to_log("error", "Error decrypting stored refresh token.")
                return {
                    'success': False,
                    'message': 'Error decrypting stored refresh token'
                }
            
            if decrypted_stored_token != refresh_token:
                print("Decrypted stored token: ", decrypted_stored_token)
                Logger.add_to_log("error", "Refresh token does not match stored token.")
                return {
                    'success': False,
                    'message': 'Refresh token does not match stored token'
                }
            
            try:
                payload = jwt.decode(
                    refresh_token,
                    cls.refresh_secret,
                    algorithms=["HS256"]
                )
            except jwt.ExpiredSignatureError:
                Logger.add_to_log("error", "Refresh token has expired.")
                return {
                    'success': False,
                    'message': 'Refresh token has expired'
                }
            except jwt.InvalidSignatureError:
                Logger.add_to_log("error", "Invalid refresh token signature.")
                return {
                    'success': False,
                    'message': 'Invalid refresh token signature'
                }
            
            required_keys = ['id', 'username', 'timezone', 'device_id']
            if not all(key in payload for key in required_keys):
                Logger.add_to_log("error", "Invalid refresh token payload structure.")
                return {
                    'success': False,
                    'message': 'Invalid refresh token payload structure'
                }
            
            token_signature_from_db = cls.tokens_service.get_token_signature_by_user_and_device(payload['id'], payload['device_id'])
            if not token_signature_from_db:
                Logger.add_to_log("error", "Token signature of refresh stored token not found.")
                return {
                    'success': False,
                    'message': 'Token signature of refresh stored token not found'
                }
            
            if token_signature_from_db != hashlib.sha256(refresh_token.encode()).hexdigest():
                Logger.add_to_log("error", "Refresh token signature does not match.")
                return {
                    'success': False,
                    'message': 'Refresh token signature does not match'
                }

            now = datetime.datetime.now(tz=pytz.timezone(payload['timezone']))
            new_access_payload = {
                'iat': now,
                'exp': now + datetime.timedelta(hours=2),
                'id': payload['id'],
                'username': payload['username'],
                'timezone': payload['timezone'],
                'device_id': payload['device_id']
            }

            new_access_token = jwt.encode(new_access_payload, cls.secret, algorithm="HS256")

            Logger.add_to_log("info", f"New access token generated for user: {payload['username']}")

            return {
                'success': True,
                'new_access_token': new_access_token,
                'device_id': new_access_payload['device_id'],
            }

        except jwt.ExpiredSignatureError:
            Logger.add_to_log("error", "Refresh token has expired.")
            return {
                'success': False,
                'message': 'Refresh token has expired'
            }
        except jwt.InvalidSignatureError:
            Logger.add_to_log("error", "Invalid refresh token signature.")
            return {
                'success': False,
                'message': 'Invalid refresh token signature'
            }
        except Exception as ex:
            Logger.add_to_log("error", f"Error verifying refresh token: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return {
                'success': False,
                'message': f"Error verifying refresh token: {str(ex)}"
            }


    @classmethod
    def decrypt_refresh_token(cls, encrypt_refresh_token):
        try:
            return cls.cipher_suite.decrypt(encrypt_refresh_token).decode()
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {
                'success': False,
                'message': f"Error decrypting refresh token: {str(ex)}"
            }
    
    @classmethod
    def validate_device(cls, user_id, device_id):
        device_exists = cls.tokens_service.device_exists(user_id, device_id)
        if not device_exists:
            Logger.add_to_log("security", f"Unregistered device for user {user_id}")
            return False
        return True
    
    @classmethod
    def refresh_token_from_cookie(cls):
        try:
            refresh_token_result = cls.get_secure_cookie('refresh_token', max_age=30 * 24 * 60 * 60)  # 30 days
            device_id_result = cls.get_secure_cookie('device_id', max_age=30 * 24 * 60 * 60)  # 30 days

            if not refresh_token_result.get('success') or not device_id_result.get('success'):
                return jsonify({
                    'success': False,
                    'message': 'Refresh token or device id not found'
                }), 401

            refresh_token = refresh_token_result['value']
            device_id = device_id_result['value']

            refresh_result = cls.verify_refresh_token(refresh_token)

            if not refresh_result.get('success'):
                return jsonify({
                    'success': False,
                    'message': refresh_result['message']
                }), 401

            if refresh_result.get('device_id') != device_id:
                Logger.add_to_log("info", "Device ID mismatch during token refresh")
                return jsonify({
                    'success': False,
                    'message': 'Invalid device',
                    'redirect': '/login'
                }), 401

            response = make_response(jsonify({
                'success': True,
                'message': 'Token refreshed successfully',
                'action': 'reload'
            }))

            cls.set_secure_cookie(
                response=response, 
                name='token', 
                value=refresh_result['new_access_token'], 
                max_age=7200
            )

            return response

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return jsonify({
                'success': False,
                'message': f"Error refreshing token: {str(ex)}"
            }), 500