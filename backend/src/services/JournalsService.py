from src.utils.Logger import Logger
from src.repositories.JournalsRepository import JournalsRepository
from src.repositories.JournalsRepository import JournalsRepository
from src.models.Journal import Journal
from datetime import datetime

class JournalsService:
    def __init__(self):
        self.journals_repository = JournalsRepository()

    def get_or_create_today_journal(self, user_id):
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
    
    def increment_interactions_count(self, user_id, journal_id):
        journal = self.journals_repository.get_journal_by_id(user_id, journal_id)
        if journal:
            self.journals_repository.increment_interactions_count(journal)
        
    def get_by_id(self, user_id, journal_id):
        try:
            return self.journals_repository.get_journal_by_id(user_id, journal_id)
        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener el registro de JournalsService: {ex}")
            raise ex
        
    def add(self, entity):
        try:
            if not isinstance(entity, Journal):
                return {"error": "Entity is not a Journal instance"}
            self.journals_repository.add(entity)
        except Exception as ex:
            Logger.add_to_log("error", f"Error al agregar el registro de JournalsService: {ex}")
            raise ex
        
    def get_journal_by_user_id_and_date(self, user_id, date):
        try:
            return self.journals_repository.get_journal_by_user_id_and_date(user_id, date)
        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener el registro de JournalsService: {ex}")
            raise ex
        
    def get_all(self, user_id):
        try:
            return self.journals_repository.find_all_by_user_id(user_id)
        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener el registro de JournalsService: {ex}")
            raise ex
        
    def get_last_journal(self, user_id):
        try:
            return self.journals_repository.find_last_by_id(user_id)
        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener el registro de JournalsService: {ex}")
            raise ex