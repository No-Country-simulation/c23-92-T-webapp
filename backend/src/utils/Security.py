import os
from dotenv import load_dotenv
import datetime
import jwt
import pytz
import traceback
from src.services.TokensService import TokensService
from cryptography.fernet import Fernet
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
    default_tz = pytz.timezone("America/New_York") # Default timezone
    tz = default_tz
    MAX_DEVICES = 5

    @classmethod
    def generate_device_id(cls):
        return str(uuid.uuid4())

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
            return {
                'success': False,
                'message': 'Device limit reached'
            }
        return {
            'success': True,
            'message': 'Device limit not reached'
        }

    @classmethod
    def get_user_timezone(cls, headers):
        tz_header = headers.get('Timezone')
        if tz_header:
            try:
                cls.tz = pytz.timezone(tz_header)
            except Exception as ex:
                cls.tz = cls.default_tz
                Logger.add_to_log("error", str(ex))
                Logger.add_to_log("error", traceback.format_exc())
        else:
            cls.tz = cls.default_tz

    @classmethod
    def generate_token(cls, authenticated_user, device_id):
        try:
            if not authenticated_user:
                Logger.add_to_log("error", "User not found.")
                return {
                    'success': False,
                    'message': 'User not found'
                }

            if not device_id:
                Logger.add_to_log("error", "Device ID missing.")
                return {
                    'success': False,
                    'message': 'Device ID missing'
                }
            
            if cls.check_device_limit(authenticated_user.id)['success'] == False:
                return {
                    'success': False,
                    'message': 'Device limit reached'
                }
            
            if cls.tokens_service.device_exists(authenticated_user.id, device_id):
                return {
                    'success': False,
                    'message': 'Device already exists for user'
                }

            active_token = cls.tokens_service.find_active_token_by_user_and_device(authenticated_user.id, device_id)

            if active_token:
                return {
                    'success': False,
                    'message': 'Active refresh token exists for current device'
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

            return {
                'success': True,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'device_id': device_id
            }
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {
                'success': False,
                'message': f"Error generating tokens: {str(ex)}"
            }

    # Verificar si el access token es valido
    @classmethod
    def verify_token(cls, headers):
        try:
            if not headers or 'Authorization' not in headers:
                Logger.add_to_log("security", "Unauthorized: Missing Authorization header")
                return {
                    'success': False,
                    'message': 'Missing Authorization header'
                }

            try:
                encoded_token = headers['Authorization'].split(" ")[1]
            except (IndexError, TypeError):
                Logger.add_to_log("security", "Invalid Authorization header format")
                return {
                    'success': False,
                    'message': 'Invalid Authorization header format'
                }

            if not cls.is_valid_token_format(encoded_token):
                return {
                    'success': False,
                    'message': 'Invalid token format'
                }

            try:
                payload = jwt.decode(
                    encoded_token, 
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
                'token_type': 'Bearer'
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
    def handle_token_refresh(cls, request_data: dict[str, any]):
        refresh_token = request_data.get('refresh_token')
        if not refresh_token:
            Logger.add_to_log("error", "Refresh token missing.")
            return {
                'success': False,
                'message': 'Refresh token missing'
            }
        
        result = cls.verify_refresh_token(refresh_token)

        return result
    
    @classmethod
    def validate_device(cls, user_id, device_id):
        device_exists = cls.tokens_service.device_exists(user_id, device_id)
        if not device_exists:
            Logger.add_to_log("security", f"Unregistered device for user {user_id}")
            return False
        return True