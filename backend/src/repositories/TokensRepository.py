from src.models.Token import Token
from extensions import db

class TokensRepository:

    def add(self, token: Token):
        db.session.add(token)
        db.session.commit()
    
    def get_by_user_id(self, user_id: str):
        return db.session.query(Token).filter(Token.user_id == user_id).first()
    
    def delete_by_user_id(self, user_id: str):
        token = self.get_by_user_id(user_id)
        if token:
            db.session.delete(token)
            db.session.commit()

    def find_last_by_user_id(self, user_id: str):
        return db.session.query(Token).filter(Token.user_id == user_id).order_by(Token.created_at.desc()).first()

    def find_last_refresh_token_by_user_id(self, user_id: str):
        return db.session.query(Token).filter(Token.user_id == user_id).order_by(Token.created_at.desc()).first().refresh_token
    
    def find_last_by_access_token(self, user_id: str):
        return db.session.query(Token).filter(Token.user_id == user_id).order_by(Token.created_at.desc()).first().access_token