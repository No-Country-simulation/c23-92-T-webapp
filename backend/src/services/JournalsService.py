from src.utils.Logger import Logger
from src.repositories.JournalsRepository import JournalsRepository
from src.repositories.UserRepository import UserRepository
from src.models.Journal import Journal
from datetime import datetime, date
import pytz
from datetime import timedelta
import uuid


INTERNAL_SERVER_ERROR = {'success': False, 'message': 'Internal server error'}, 500

class JournalsService:
    def __init__(self):
        self.journals_repository = JournalsRepository()
        self.user_repository = UserRepository()

    def get_or_create_today_journal(self, user_id):
        try:
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

            today_journal = self.journals_repository.find_by_date_range(
                user_id, 
                today_start, 
                today_end
            )

            if today_journal:
                return today_journal

            new_journal = Journal(user_id=user_id)
            self.journals_repository.add(new_journal)
            return new_journal
        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener o crear el journal: {ex}")
            return INTERNAL_SERVER_ERROR
    
    def increment_interactions_count(self, user_id, journal_id):
        try:
            journal = self.journals_repository.get_journal_by_id(user_id, journal_id)
            if journal:
                self.journals_repository.increment_interactions_count(journal)
        except Exception as ex:
            Logger.add_to_log("error", f"Error al incrementar el contador de interacciones: {ex}")
            return INTERNAL_SERVER_ERROR
        
    def get_by_id(self, user_id, journal_id):
        try:
            return self.journals_repository.get_journal_by_id(user_id, journal_id)
        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener el registro de JournalsService: {ex}")
            return INTERNAL_SERVER_ERROR
        
    def add(self, entity):
        try:
            if not isinstance(entity, Journal):
                return {"error": "Entity is not a Journal instance"}
            self.journals_repository.add(entity)
        except Exception as ex:
            Logger.add_to_log("error", f"Error al agregar el registro de JournalsService: {ex}")
            return INTERNAL_SERVER_ERROR
        
    def get_journal_by_user_id_and_date(self, user_id, date):
        try:
            return self.journals_repository.get_journal_by_user_id_and_date(user_id, date)
        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener el registro de JournalsService: {ex}")
            return INTERNAL_SERVER_ERROR
        
    def get_all(self, user_id):
        try:
            journals = self.journals_repository.find_all_by_user_id(user_id)
            journals_dict = [journal.to_dict() for journal in journals]
            return journals_dict
        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener el registro de JournalsService: {ex}")
            return INTERNAL_SERVER_ERROR
        
    def get_last_journal(self, user_id):
        try:
            return self.journals_repository.find_last_by_id(user_id)
        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener el registro de JournalsService: {ex}")
            return INTERNAL_SERVER_ERROR
        
    def find_journal_of_today_by_id(self, user_id, user_timezone='UTC'):
        try:
            user_tz = pytz.timezone(user_timezone)
            user_now = datetime.now(user_tz)

            today_start = user_now.replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1) - timedelta(microseconds=1)

            today_start_utc = today_start.astimezone(pytz.UTC)
            today_end_utc = today_end.astimezone(pytz.UTC)

            journal = self.journals_repository.find_by_date_range(user_id, today_start_utc, today_end_utc)

            Logger.add_to_log("info", f"Journal found: {journal}")

            return journal
        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener el journal del día: {ex}")
            raise  # Relanza la excepción para manejarla en el lugar adecuado

    from datetime import date  # Importar date directamente

    def get_journal_for_day(self, user_id, target_date):
        """
        Get the journal for a specific day with its mood_journal_intensity.
        Args:
            user_id (str, int, UUID): The ID of the user.
            target_date (datetime.date): The target date as a date object.
            timezone (str): The user's timezone (default is UTC).
        Returns:
            dict: Success status and data with journal details and mood_journal_intensity.
        """
        try:
            if not isinstance(user_id, (str, int, uuid.UUID)):
                return {"success": False, "error": "Invalid user id, must be a string, integer or UUID"}

            if not isinstance(target_date, date):
                return {"success": False, "error": "Invalid target_date, must be a datetime.date object"}

            timezone = self.user_repository.get_timezone(user_id=str(user_id))
            try:
                tz = pytz.timezone(timezone)
            except pytz.UnknownTimeZoneError:
                tz = pytz.timezone("UTC")

            result = self.journals_repository.get_journal_with_intensity(user_id, target_date, str(tz))
            return result

        except Exception as ex:
            Logger.add_to_log("error", f"Error en get_journal_for_day: {ex}")
            return {"success": False, "error": "Internal server error"}