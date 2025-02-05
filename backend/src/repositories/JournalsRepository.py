from extensions import db
from src.models.Journal import Journal
from datetime import datetime
from src.utils.Logger import Logger
from datetime import datetime
from pytz import timezone as tz_timezone
import pytz
from collections import Counter

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
        return db.session.query(Journal).filter(Journal.user_id == user_id).order_by(Journal.date_journal.desc()).all()
    
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
    
    def get_journals_in_range(self, user_id, start_date, end_date):
        return db.session.query(Journal).filter(
            Journal.user_id == user_id,
            Journal.date_journal >= start_date,
            Journal.date_journal <= end_date
        ).all()

    def get_journal_with_intensity(self, user_id, target_date, timezone="UTC"):
        """
        Get the journal for a specific date with its average mood intensity and most frequent mood state.
        Args:
            user_id (str, int, UUID): The ID of the user.
            target_date (datetime.date): The target date to filter the journal.
            timezone (str): The user's timezone (default is UTC).
        Returns:
            dict: Journal data with interactions, mood_journal_intensity, and mood_mode.
        """
        try:
            if not isinstance(timezone, str):
                raise ValueError("Invalid timezone, must be a string")

            try:
                user_tz = tz_timezone(timezone)
            except pytz.UnknownTimeZoneError:
                raise ValueError(f"Unknown timezone: {timezone}")

            start_of_day = user_tz.localize(datetime.combine(target_date, datetime.min.time()))
            end_of_day = user_tz.localize(datetime.combine(target_date, datetime.max.time()))

            start_of_day_utc = start_of_day.astimezone(tz_timezone("UTC"))
            end_of_day_utc = end_of_day.astimezone(tz_timezone("UTC"))

            journal = (
                db.session.query(Journal)
                .filter(
                    Journal.user_id == user_id,
                    Journal.date_journal >= start_of_day_utc,
                    Journal.date_journal <= end_of_day_utc
                )
                .first()
            )

            if not journal:
                return {"success": True, "data": None}

            total_intensity = sum(
                interaction.mood_intensity for interaction in journal.interactions if interaction.mood_intensity is not None
            )
            total_interactions = len(
                [interaction for interaction in journal.interactions if interaction.mood_intensity is not None]
            )
            mood_journal_intensity = round(total_intensity / total_interactions, 2) if total_interactions > 0 else 0

            mood_states = [interaction.state_interaction for interaction in journal.interactions if interaction.state_interaction is not None]
            if mood_states:
                mood_mode = Counter(mood_states).most_common(1)[0][0]
            else:
                mood_mode = None

            formatted_journal = {
                "date_journal": journal.date_journal.astimezone(user_tz).isoformat(),
                "interactions_count": journal.interactions_count,
                "mood_journal_intensity": mood_journal_intensity,
                "mood_mode": mood_mode,
                "interactions": [interaction.to_dict_without_journal() for interaction in journal.interactions],
            }

            return {"success": True, "data": formatted_journal}

        except Exception as ex:
            Logger.add_to_log("error", f"Error en get_journal_with_intensity: {ex}")
            return {"success": False, "error": "Internal server error"}