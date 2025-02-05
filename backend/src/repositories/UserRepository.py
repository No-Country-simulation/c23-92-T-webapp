from extensions import db
from src.models.User import User

class UserRepository:
    def get_all(self):
        return db.session.query(User).all()
    
    def get_by_id(self, id):
        return db.session.query(User).filter_by(id=id).first()

    def add(self, entity):
        db.session.add(entity)
        db.session.commit()

    def delete(self, entity):
        db.session.delete(entity)
        db.session.commit()

    def update(self):
        db.session.commit()

    def get_user_by_username(self, username):
        return db.session.query(User).filter_by(username=username).first()

    def get_user_by_email(self, email):
        return db.session.query(User).filter_by(email=email).first()
    
    def update_password(self, user_id, new_password):
        user = self.get_by_id(user_id)
        user.password = user.encrypt_password(new_password)
        db.session.commit()
        return user
    
    def get_timezone(self, user_id):
        user = self.get_by_id(user_id)
        return user.timezone

    def update_username(self, user_id, username):
        username_exists = self.get_user_by_username(username)
        if username_exists:
            return None
        user = self.get_by_id(user_id)
        user.username = username
        db.session.commit()
        return user

    def update_email(self, user_id, email):
        email_exists = self.get_user_by_email(email)
        if email_exists:
            return None
        user = self.get_by_id(user_id)
        user.email = email
        db.session.commit()
        return user
    
    def update_timezone(self, user_id, timezone):
        user = self.get_by_id(user_id)
        user.timezone = timezone
        db.session.commit()
        return user