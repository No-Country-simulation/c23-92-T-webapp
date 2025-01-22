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