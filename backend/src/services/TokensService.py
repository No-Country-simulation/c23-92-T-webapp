from src.models.Token import Token
from src.repositories.TokensRepository import TokensRepository
from src.utils.Logger import Logger
import traceback

INTERNAL_SERVER_ERROR={'success': False, 'message': 'Internal server error'}, 500

class TokensService:
    def __init__(self):
        self.token_repository = TokensRepository()

    def create_token(self, user_id: int, token_signature, refresh_token, expires_at, device_id) -> Token:
        try:
            token = Token(user_id=user_id, token_signature=token_signature, refresh_token=refresh_token, expires_at=expires_at, device_id=device_id)
            self.token_repository.add(token)
            return token
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR
    
    def find_last_by_user_id(self, user_id: str) -> Token:
        try:
            return self.token_repository.find_last_by_user_id(user_id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR
    
    def find_last_refresh_token_by_user_id(self, user_id: str) -> str:
        try:
            return self.token_repository.find_last_refresh_token_by_user_id(user_id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR
        
    def find_active_token_by_user_id(self, user_id: str) -> Token:
        try:
            return self.token_repository.find_active_token_by_user_id(user_id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR
        
    def revoke_old_tokens(self, user_id: str) -> bool:
        try:
            self.token_repository.revoke_old_tokens(user_id)
            return True
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR
        
    def cleanup_expired_token(self, user_timezone) -> None:
        try:
            self.token_repository.cleanup_expired_token(user_timezone)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR
    
    def get_token_signature_by_user_id(self, user_id: str) -> str:
        try:
            return self.token_repository.get_token_signature_by_user_id(user_id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR
        
    def find_active_token_by_user_and_device(self, user_id: str, device_id: str) -> Token:
        try:
            return self.token_repository.find_active_token_by_user_and_device(user_id, device_id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR
        
    def revoke_old_tokens_for_device(self, user_id: str, device_id: str) -> None:
        try:
            self.token_repository.revoke_old_tokens_for_device(user_id, device_id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR
        
    def get_token_signature_by_user_and_device(self, user_id: str, device_id: str) -> str:
        try:
            return self.token_repository.get_token_signature_by_user_and_device(user_id, device_id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR
        
    def count_active_devices_by_user(self, user_id: str) -> int:
        try:
            return self.token_repository.count_active_devices_by_user(user_id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR
        
    def device_exists(self, user_id: str, device_id: str) -> bool:
        try:
            return self.token_repository.device_exists(user_id, device_id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR 
        
    def get_all_tokens_by_username(self, username: str) -> list:
        try:
            tokens = self.token_repository.get_tokens_by_username(username)
            return [token.to_dict() for token in tokens]
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR
        
    def get_oldest_active_token(self, user_id: str) -> Token:
        try:
            return self.token_repository.get_oldest_active_token(user_id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR
        
    def revoke_token(self, token_id: str):
        try:
            self.token_repository.revoke_token(token_id)
            return True
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return INTERNAL_SERVER_ERROR