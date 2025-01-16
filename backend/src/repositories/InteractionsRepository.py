from extensions import db
from src.models.Interactions import Interactions

class InteractionsRepository:
    def get_all(self):
        return db.session.query(Interactions).all()
    
    def get_by_id(self, id):
        return db.session.query(Interactions).filter_by(id=id).first()

    def add(self, entity):
        db.session.add(entity)
        db.session.commit()

    def delete(self, entity):
        db.session.delete(entity)
        db.session.commit()

    def update(self):
        db.session.commit()

    #crear get_by_date()