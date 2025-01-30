from src.models.Token import Token
from extensions import db
from datetime import datetime
from src.models.User import User

class TokensRepository:

    def add(self, token: Token):
        db.session.add(token)
        db.session.commit()

    def find_active_token_by_user_and_device(self, user_id: str, device_id: str):
        return db.session.query(Token).filter(Token.user_id == user_id, Token.device_id == device_id, Token.is_revoked == False).first()

    def find_active_token_by_user_id(self, user_id: str):
        return db.session.query(Token).filter(Token.user_id == user_id, Token.is_revoked == False).order_by(Token.created_at.desc()).first()

    def find_last_by_user_id(self, user_id: str):
        return db.session.query(Token).filter(Token.user_id == user_id).order_by(Token.created_at.desc()).first()

    def find_last_refresh_token_by_user_id(self, user_id: str):
        return db.session.query(Token).filter(Token.user_id == user_id).order_by(Token.created_at.desc()).first().refresh_token
        
    def revoke_old_tokens(self, user_id: str):
        db.session.query(Token).filter(Token.user_id == user_id).update({Token.is_revoked: True})
        db.session.commit()

    def cleanup_expired_token(self, user_timezone) -> None:
        db.session.query(Token).filter(Token.expires_at < datetime.now(user_timezone), Token.is_revoked == False).update({Token.is_revoked: True})
        db.session.commit()

    def get_token_signature_by_user_id(self, user_id: str):
        return db.session.query(Token).filter(Token.user_id == user_id).order_by(Token.created_at.desc()).first().token_signature
    
    def revoke_old_tokens_for_device(self, user_id: str, device_id: str):
        db.session.query(Token).filter(Token.user_id == user_id, Token.device_id == device_id).update({Token.is_revoked: True})
        db.session.commit()

    def get_token_signature_by_user_and_device(self, user_id: str, device_id: str):
        return db.session.query(Token).filter(Token.user_id == user_id, Token.device_id == device_id, Token.is_revoked == False).order_by(Token.created_at.desc()).first().token_signature
    
    def count_active_devices_by_user(self, user_id: str):
        return db.session.query(Token).filter(Token.user_id == user_id, Token.is_revoked == False).count()

    def device_exists(self, user_id: str, device_id: str):
        return db.session.query(Token).filter(Token.user_id == user_id, Token.device_id == device_id).count() > 0
    
    def get_tokens_by_username(self, username: str):
        return db.session.query(Token).join(User).filter(User.username == username).all()
    
    def get_oldest_active_token(self, user_id: str):
        return db.session.query(Token).filter(Token.user_id == user_id, Token.is_revoked == False).order_by(Token.created_at).first()
    
    def revoke_token(self, token_id: str):
        db.session.query(Token).filter(Token.id == token_id).update({Token.is_revoked: True})
        db.session.commit()