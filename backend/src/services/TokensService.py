from src.models.Token import Token
from src.repositories.TokensRepository import TokensRepository
from src.utils.Logger import Logger
import traceback

class TokensService:
    def __init__(self):
        self.token_repository = TokensRepository()

    def create_token(self, user_id: int, refresh_token, expires_at) -> Token:
        try:
            token = Token(user_id=user_id, refresh_token=refresh_token, expires_at=expires_at)
            self.token_repository.add(token)
            return token
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            raise ex

    def delete_token(self, user_id: str) -> bool:
        try:
            self.token_repository.delete_by_user_id(user_id)
            return True
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            raise ex
    
    def find_last_by_user_id(self, user_id: str) -> Token:
        try:
            return self.token_repository.find_last_by_user_id(user_id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            raise ex
    
    def find_last_refresh_token_by_user_id(self, user_id: str) -> str:
        try:
            return self.token_repository.find_last_refresh_token_by_user_id(user_id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            raise ex
    
    def find_last_by_access_token(self, user_id: str) -> str:
        try:
            return self.token_repository.find_last_by_access_token(user_id)
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            raise ex