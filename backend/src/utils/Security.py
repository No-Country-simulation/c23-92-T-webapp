import os
from dotenv import load_dotenv
import datetime
import jwt
import pytz
import traceback
from src.models.Token import Token
from src.services.TokensService import TokensService
from cryptography.fernet import Fernet

# Logger
from src.utils.Logger import Logger

load_dotenv()

class Security():

    tokens_service = TokensService()

    refresh_encryption_key = os.getenv("REFRESH_ENCRYPTION_KEY")
    cipher_suite = Fernet(refresh_encryption_key)
    secret = os.getenv("SECRET_KEY")
    refresh_secret = os.getenv("REFRESH_SECRET_KEY")
    default_tz = pytz.timezone("America/New_York") # Default timezone
    tz = default_tz

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
    def generate_token(cls, authenticated_user):
        try:
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
                'timezone': cls.tz.zone
            }

            Logger.add_to_log("info", f"Generating token with timezone: {cls.tz.zone}")

            access_token = jwt.encode(payload, cls.secret, algorithm="HS256")

            refresh_payload = {
                'iat': now,
                'exp': now + datetime.timedelta(days=30),
                'id': str(authenticated_user.id),
                'username': authenticated_user.username,
                'timezone': cls.tz.zone
            }

            Logger.add_to_log("info", f"Generating refresh token with timezone: {cls.tz.zone}")

            refresh_token = jwt.encode(refresh_payload, cls.refresh_secret, algorithm="HS256")

            cls.tokens_service.create_token(user_id=authenticated_user.id, refresh_token=cls.cipher_suite.encrypt(refresh_token.encode()).decode(), expires_at=payload['exp'])

            return access_token, refresh_token
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def generate_access_token(cls, authenticated_user):
        try:
            try:
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
                'timezone': cls.tz.zone
            }

            Logger.add_to_log("info", f"Generating token with timezone: {cls.tz.zone}")

            access_token = jwt.encode(payload, cls.secret, algorithm="HS256")

            return access_token
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())


    @classmethod
    def verify_token(cls, headers):
        try:
            print("Headers: ", headers)
            if 'Authorization' not in headers.keys():
                print("Headers available: ", headers.keys())
                Logger.add_to_log("error", "Authorization header missing or malformed.")
                return False

            authorization = headers['Authorization']
            print("Authorization: ", authorization)
            encoded_token = authorization.split(" ")[1]
            print("Token extraido", encoded_token)
            Logger.add_to_log("info", f"Verifying token: {encoded_token}")

            if not cls.is_valid_token_format(encoded_token):
                Logger.add_to_log("error", "Invalid token format.")
                return False
            print(encoded_token)
            payload = cls.decode_token(encoded_token)
            if not payload:
                return False

            if not cls.is_valid_payload(payload):
                Logger.add_to_log("error", "Invalid token payload structure.")
                return False

            return cls.is_token_active(encoded_token, payload)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return False

    @classmethod
    def is_valid_token_format(cls, token):
        return len(token) > 0 and token.count('.') == 2

    @classmethod
    def decode_token(cls, token):
        try:
            return jwt.decode(token, cls.secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            Logger.add_to_log("error", "Token has expired.")
        except jwt.InvalidSignatureError:
            Logger.add_to_log("info", token)
            Logger.add_to_log("error", "Invalid token signature.")
        return None

    @classmethod
    def is_valid_payload(cls, payload):
        required_keys = ['id', 'username', 'timezone']
        return all(key in payload for key in required_keys)

    @classmethod
    def is_token_active(cls, token, payload):
        Logger.add_to_log("info", f"Token verified for user: {payload['username']}")

        exp_datetime = datetime.datetime.fromtimestamp(payload["exp"], tz=pytz.timezone(payload['timezone']))

        current_datetime = datetime.datetime.now(tz=pytz.timezone(payload['timezone']))

        if token and exp_datetime > current_datetime:
            return True
        Logger.add_to_log("error", "Token no encontrado o ha expirado.")
        return False



    @classmethod
    def verify_refresh_token(cls, refresh_token: str):
        try:
            unverified_payload = jwt.decode(
                refresh_token,
                cls.refresh_secret,
                algorithms=["HS256"],
                options={"verify-exp": False}
            )

            stored_token = cls.tokens_service.find_last_by_user_id(unverified_payload['id'])
            if not stored_token:
                Logger.add_to_log("error", "No refresh token found for user.")
                return False, None

            decrypted_stored_token = cls.decrypt_refresh_token(stored_token.refresh_token)
            if not decrypted_stored_token:
                Logger.add_to_log("error", "Error decrypting stored refresh token.")
                return False, None
            
            if decrypted_stored_token != refresh_token:
                print("Decrypted stored token: ", decrypted_stored_token)
                Logger.add_to_log("error", "Refresh token does not match stored token.")
                return False, None
            
            try:
                payload = jwt.decode(
                    refresh_token,
                    cls.refresh_secret,
                    algorithms=["HS256"]
                )
            except jwt.ExpiredSignatureError:
                Logger.add_to_log("error", "Refresh token has expired.")
                return False, None
            except jwt.InvalidSignatureError:
                Logger.add_to_log("error", "Invalid refresh token signature.")
                return False, None
            
            required_keys = ['id', 'username', 'timezone']
            if not all(key in payload for key in required_keys):
                Logger.add_to_log("error", "Invalid refresh token payload structure.")
                return False, None

            now = datetime.datetime.now(tz=pytz.timezone(payload['timezone']))
            new_access_payload = {
                'iat': now,
                'exp': now + datetime.timedelta(hours=2),
                'id': payload['id'],
                'username': payload['username'],
                'timezone': payload['timezone']
            }

            new_access_token = jwt.encode(new_access_payload, cls.secret, algorithm="HS256")

            Logger.add_to_log("info", f"New access token generated for user: {payload['username']}")
            return True, new_access_token

        except jwt.ExpiredSignatureError:
            Logger.add_to_log("error", "Refresh token has expired.")
            return False, None
        except jwt.InvalidSignatureError:
            Logger.add_to_log("error", "Invalid refresh token signature.")
            return False, None
        except Exception as ex:
            Logger.add_to_log("error", f"Error in verify_refresh_token: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            return False, None


    @classmethod
    def decrypt_refresh_token(cls, encrypt_refresh_token):
        try:
            return cls.cipher_suite.decrypt(encrypt_refresh_token).decode()
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def handle_token_refresh(cls, request_data: dict[str, any]):
        refresh_token = request_data.get('refresh_token')
        if not refresh_token:
            Logger.add_to_log("error", "Refresh token missing.")
            return False, None
        
        success, new_access_token = cls.verify_refresh_token(refresh_token)

        if not success or not new_access_token:
            return None
        
        return {
            'access_token': new_access_token,
            'tokey_type': 'Bearer'
        }