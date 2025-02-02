from extensions import db
from src.models.Interactions import Interactions
from sqlalchemy import func, cast, Float
from src.models.Journal import Journal

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

    def get_interactions_by_journal_id(self, journal_id):
        return db.session.query(Interactions).filter(
            Interactions.journal_id == journal_id
        ).all()
    
    def get_mood_evolution(self, user_id, start_date, end_date):
        return (
            db.session.query(
                func.date(Interactions.date_interaction).label('date'),
                Interactions.state_interaction,
                cast(func.avg(Interactions.mood_intensity), Float).label('avg_intensity')
            )
            .join(Journal, Journal.id == Interactions.journal_id)
            .filter(Journal.user_id == user_id)
            .filter(Interactions.date_interaction >= start_date)
            .filter(Interactions.date_interaction <= end_date)
            .group_by(func.date(Interactions.date_interaction), Interactions.state_interaction)
            .order_by(func.date(Interactions.date_interaction))
            .all()
        )
    
    def get_all_interactions_by_user(self, user_id):
        return (
            db.session.query(Interactions)
            .join(Journal, Journal.id == Interactions.journal_id)
            .filter(Journal.user_id == user_id)
            .order_by(Interactions.date_interaction.desc())
            .all()
        )