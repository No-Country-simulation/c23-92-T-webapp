from decouple import config

import datetime
import jwt
import pytz
import traceback

# Logger
from src.utils.Logger import Logger


class Security():

    secret = config('JWT_KEY')
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
    def generate_token(cls, authenticated_user, headers):
        try:
            cls.get_user_timezone(headers)
            payload = {
                'iat': datetime.datetime.now(tz=cls.tz),
                'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(hours=2),
                'username': authenticated_user.username,
                'fullname': authenticated_user.fullname,
            }
            access_token = jwt.encode(payload, cls.secret, algorithm="HS256")

            refresh_payload = {
                'iat': datetime.datetime.now(tz=cls.tz),
                'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(days=30),
                'username': authenticated_user.username,
            }
            refresh_token = jwt.encode(refresh_payload, cls.refresh_secret, algorithm="HS256")

            return access_token, refresh_token
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def verify_token(cls, headers):
        try:
            if 'Authorization' in headers.keys():
                authorization = headers['Authorization']
                encoded_token = authorization.split(" ")[1]

                if ((len(encoded_token) > 0) and (encoded_token.count('.') == 3)):
                    try:
                        payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])

                        timezone = payload.get('timezone', cls.tz.zone)

                        if timezone == cls.tz.zone:
                            return True
                        return False
                    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                        return False

            return False
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())


    @classmethod
    def verify_refresh_token(cls, refresh_token):
        try:
            payload = jwt.decode(refresh_token, cls.refresh_secret, algorithms=["HS256"])
            if payload:
                return True
            return False
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            return False
