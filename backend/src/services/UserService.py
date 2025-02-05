from src.repositories.UserRepository import UserRepository
from src.repositories.TokensRepository import TokensRepository
from src.utils.Logger import Logger
import traceback
import pytz

INTERNAL_SERVER_ERROR = 'Internal server error'

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.tokens_repository = TokensRepository()

    def update_timezone(self, user_id: int, new_timezone: str):
        try:
            if new_timezone not in pytz.all_timezones:
                return {
                    'success': False,
                    'error': 'Invalid timezone'
                }
            
            user = self.user_repository.get_by_id(user_id)
            if not user:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            user.timezone = new_timezone

            self.user_repository.update(user)

            return {
                'success': True,
                'message': 'Timezone updated successfully'
            }
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {
                'success': False,
                'error': INTERNAL_SERVER_ERROR
            }
        
    def get_timezone(self, user_id: int):
        try:
            timezone = self.user_repository.get_timezone(user_id)
            if not timezone:
                return {
                    'success': False,
                    'error': 'User not found and timezone not set'
                }
            return {
                'success': True,
                'timezone': timezone
            }
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {
                'success': False,
                'error': INTERNAL_SERVER_ERROR
            }
        
    def delete_account(self, user_id: int):
        try:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            self.tokens_repository.delete_all_by_user_id(user_id=user_id)
            self.user_repository.delete(user)

            return {
                'success': True,
                'message': 'Account deleted successfully'
            }
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {
                'success': False,
                'error': INTERNAL_SERVER_ERROR
            }