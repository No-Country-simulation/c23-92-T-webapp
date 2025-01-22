from extensions import db
from src.models.Interactions import Interactions
from src.services.JournalsService import JournalsService

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

    def get_interactions_by_journal_id(self, user_id, journal_id):
        journal_service = JournalsService()
        journal = journal_service.get_by_id(user_id, journal_id)
        return db.session.query(Interactions).filter(Interactions.journal_id == journal.id).all()