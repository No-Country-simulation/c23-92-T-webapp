from extensions import db
from src.models.Journal import Journal
from datetime import datetime, timedelta
import pytz

class JournalsRepository:
    def get_all(self):
        return db.session.query(Journal).all()
    
    def find_last_by_id(self, user_id):
        return db.session.query(Journal).filter(Journal.user_id == user_id).order_by(Journal.date_journal.desc()).first()


    def add(self, entity):
        db.session.add(entity)
        db.session.commit()

    def delete(self, entity):
        db.session.delete(entity)
        db.session.commit()

    def update(self):
        db.session.commit()

    def increment_interactions_count(self, entity):
        entity.interactions_count += 1
        db.session.commit()

    def find_by_date_range(self, user_id, start, end):
        return db.session.query(Journal).filter(
            Journal.user_id == user_id,
            Journal.date_journal >= start,
            Journal.date_journal <= end
        ).first()
    
    def find_all_by_user_id(self, user_id):
        return db.session.query(Journal).filter(Journal.user_id == user_id).all()
    
    def find_journal_of_today_by_id(self, user_id, user_timezone='UTC'):
        user_tz = pytz.timezone(user_timezone)
        user_now = datetime.now(user_tz)

        today_start = user_now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1) - timedelta(microseconds=1)

        today_start_utc = today_start.astimezone(pytz.UTC)
        today_end_utc = today_end.astimezone(pytz.UTC)

        return self.find_by_date_range(user_id, today_start_utc, today_end_utc)
    
    def get_journal_by_user_id_and_date(self, user_id, date):
        return db.session.query(Journal).filter(
            Journal.user_id == user_id,
            Journal.date_journal == date
        ).first()
    
    def get_journal_by_id(self, user_id, id):
        return db.session.query(Journal).filter(
            Journal.user_id == user_id,
            Journal.id == id
        ).first()