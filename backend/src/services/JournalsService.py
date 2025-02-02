from src.utils.Logger import Logger
from src.repositories.JournalsRepository import JournalsRepository
from src.repositories.JournalsRepository import JournalsRepository
from src.models.Journal import Journal
from datetime import datetime
import pytz
from datetime import timedelta

INTERNAL_SERVER_ERROR = {'success': False, 'message': 'Internal server error'}, 500

class JournalsService:
    def __init__(self):
        self.journals_repository = JournalsRepository()

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