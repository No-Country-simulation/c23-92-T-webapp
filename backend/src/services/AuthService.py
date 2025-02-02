import traceback
from src.utils.Logger import Logger
from src.models.User import User
from src.repositories.UserRepository import UserRepository
from src.repositories.TokensRepository import TokensRepository
import pytz
import re


class AuthService():
    def __init__(self):
        self.user_repository = UserRepository()
        self.tokens_repository = TokensRepository()

    def login_user(self, username, password):
        try:
            username = username.strip()
            username = username.lower()
            password = password.strip()
            user = self.user_repository.get_user_by_username(username)
            if not user:
                Logger.add_to_log("error", "User not found")
                return {'success': False, 'message': 'User not found'}
            Logger.add_to_log("check_password", user.check_password(password))
            print(user.check_password(password))
            if user and user.check_password(password):
                return user
            return {'success': False, 'message': 'Invalid credentials'}
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'success': False, 'message': 'Internal server error'}
        

    def register_user(self, username, email, password, timezone="UTC"):
        try:
            if not all([username, email, password]):
                return {'success': False, 'message': 'Username, email and password are required'}

            username = username.strip()
            username = username.lower()
            email = email.strip()
            password = password.strip()
            timezone = timezone.strip()
            
            if not (3 <= len(username) <= 20):
                return {'success': False, 'message': 'Username must be between 3 and 20 characters'}

            email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not re.match(email_pattern, email):
                return {'success': False, 'message': 'Invalid email format'}

            if not self._validate_password(password):
                return {
                    'success': False, 
                    'message': 'Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number and one special character'
                }

            if self.user_repository.get_user_by_username(username):
                return {'success': False, 'message': 'Username already exists'}
            
            if self.user_repository.get_user_by_email(email):
                return {'success': False, 'message': 'Email already exists'}
            
            if timezone not in pytz.all_timezones:
                return {'success': False, 'message': 'Invalid timezone'}
            
            user = User(username=username, email=email, password=password, timezone=timezone)
            self.user_repository.add(user)
            return {'success': True, 'message': 'User registered successfully'}
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'success': False, 'message': 'Internal server error'}
        
    def _validate_password(self, password):
        if len(password) < 8:
            return False
            
        if not re.search(r'[A-Z]', password):
            return False
            
        if not re.search(r'[a-z]', password):
            return False
            
        if not re.search(r'\d', password):
            return False
            
        special_chars = r'[!"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~]'
        if not re.search(special_chars, password):
            return False
            
        return True
        
    def logout_user(self, user_id, device_id):
        try:
            self.tokens_repository.revoke_old_tokens_for_device(user_id, device_id)
            return {
                'success': True,
                'message': 'User logged out successfully'
            }
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {
                'sucess': False,
                'message': 'Logout failed'
            }
    
    def change_password(self, user_id, old_password, new_password):
        try:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                return {
                    'success': False,
                    'message': 'User not found'
                }
            
            if not user.check_password(old_password):
                return {
                    'success': False,
                    'message': 'Incorrect current password'
                }
            
            if len(new_password) < 8:
                return {
                    'success': False,
                    'message': 'Password must be at least 8 characters long'
                }
            
            password_changed = self.user_repository.update_password(user_id, new_password)

            if not password_changed:
                return {
                    'success': False,
                    'message': 'Password change failed'
                }

            self.tokens_repository.revoke_old_tokens(user_id)

            return {
                'success': True,
                'message': 'Password updated successfully'
            }
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {
                'success': False,
                'message': 'Password changed failed'
            }