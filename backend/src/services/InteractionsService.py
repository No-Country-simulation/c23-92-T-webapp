from src.repositories.InteractionsRepository import InteractionsRepository
from src.services.JournalsService import JournalsService
from src.models.Interactions import Interactions
from src.utils.Logger import Logger

INTERNAL_SERVER_ERROR = {'success': False, 'message': 'Internal server error'}, 500

class InteractionsService:
    def __init__(self):
        self.interactions_repository = InteractionsRepository()
        self.journals_service = JournalsService()

    def create_interaction(self, user_id, title, state, content, response):
        try:
            journal = self.journals_service.get_or_create_today_journal(user_id)
            interaction = Interactions(title=title, state=state, content=content, response=response, journal_id=journal.id)
            self.interactions_repository.add(interaction)
            self.journals_service.increment_interactions_count(user_id=user_id, journal_id=journal.id)
            return interaction
        except Exception as ex:
            Logger.add_to_log("error", f"Error al crear la interacción en InteractionsService: {ex}")
            return INTERNAL_SERVER_ERROR
        
    def list_interactions_by_journal(self, user_id, journal_id):
        try:
            return self.interactions_repository.get_by_journal_id(user_id, journal_id)
        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener las interacciones en InteractionsService: {ex}")
            return INTERNAL_SERVER_ERROR
