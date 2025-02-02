from src.repositories.InteractionsRepository import InteractionsRepository
from src.services.JournalsService import JournalsService
from src.models.Interactions import Interactions
from src.utils.Logger import Logger

INTERNAL_SERVER_ERROR = {'success': False, 'message': 'Internal server error'}, 500

class InteractionsService:
    def __init__(self):
        self.interactions_repository = InteractionsRepository()
        self.journals_service = JournalsService()

    def create_interaction(self, user_id, title, state, content, response, mood_intensity=None):
        try:
            journal = self.journals_service.get_or_create_today_journal(user_id)
            interaction = Interactions(title=title, state=state, content=content, response=response, journal_id=journal.id, mood_intensity=mood_intensity)
            self.interactions_repository.add(interaction)
            self.journals_service.increment_interactions_count(user_id=user_id, journal_id=journal.id)
            return interaction
        except Exception as ex:
            Logger.add_to_log("error", f"Error al crear la interacción en InteractionsService: {ex}")
            return INTERNAL_SERVER_ERROR
        
    def list_interactions_by_journal(self, user_id, journal_id):
        try:
            Logger.add_to_log("info", f"Journal id: {journal_id}")
            journal_id_verified = self.journals_service.get_by_id(user_id, journal_id)
            Logger.add_to_log("info", f"Journal id verified: {journal_id_verified}")
            if not journal_id_verified:
                return {"error": "Journal not found"}
            Logger.add_to_log("info", f"Journal id verified: {journal_id_verified.id}")
            interactions = self.interactions_repository.get_interactions_by_journal_id(journal_id_verified.id)

            interactions_dict = [interactions.to_dict() for interactions in interactions]
            Logger.add_to_log("info", f"Interactions found: {interactions_dict}")
            return interactions_dict
        except Exception as ex:
            Logger.add_to_log("error", f"Error al obtener las interacciones en InteractionsService: {ex}")
            return INTERNAL_SERVER_ERROR