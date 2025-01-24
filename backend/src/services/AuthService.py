import traceback
from src.utils.Logger import Logger
from src.models.User import User
from src.repositories.UserRepository import UserRepository
from src.repositories.TokensRepository import TokensRepository
import pytz


class AuthService():
    def __init__(self):
        self.user_repository = UserRepository()
        self.tokens_repository = TokensRepository()

    def login_user(self, username, password):
        try:
            user = self.user_repository.get_user_by_username(username)
            if user and user.check_password(password):
                return user
            return {'success': False, 'message': 'Invalid credentials'}
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'success': False, 'message': 'Internal server error'}
        

    def register_user(self, username, email, password, timezone="UTC"):
        try:
            if not username or not password:
                return {'success': False, 'message': 'Username and password are required'}
            
            if len(password) < 8:
                return {'success': False, 'message': 'Password must be at least 8 characters long'}

            if self.user_repository.get_user_by_username(username):
                return {'success': False, 'message': 'Username already exists'}
            
            if self.user_repository.get_user_by_email(email):
                return {'success': False, 'message': 'Email already exists'}
            
            if timezone not in pytz.all_timezones:
                return {'success': False, 'message': 'Invalid timezone'}
            
            user = User(username=username, email=email, password=password, timezone=timezone)
            self.user_repository.add(user)
            return {'success': True, 'message': 'User created'}
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'success': False, 'message': 'Internal server error'}
        
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