from src.repositories.UserRepository import UserRepository
from src.utils.Logger import Logger
import traceback
import pytz

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

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
                'error': 'Internal server error'
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
                'error': 'Internal server error'
            }