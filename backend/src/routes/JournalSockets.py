from src.services.InteractionsService import InteractionsService
from src.services.JournalsService import JournalsService
from src.services.UserService import UserService
from src.services.MoodEvolutionService import MoodEvolutionService
from src.services.WordCloudService import WordCloudService
from src.services.MoodPieChartService import MoodPieChartService
from src.middlewares.SocketAuthMiddleware import SocketAuthMiddleware
from flask_socketio import emit
from src.utils.Logger import Logger
import uuid

INTERNAL_SERVER_ERROR = "Internal server error"

def register_journal_events(socketio):
    interactions_service = InteractionsService()
    journals_service = JournalsService()
    users_service = UserService()
    mood_evolution_service = MoodEvolutionService()
    word_cloud_service = WordCloudService()
    mood_pie_char_service = MoodPieChartService()

    @socketio.on('get_interactions_of_today')
    @SocketAuthMiddleware.require_auth
    def handle_get_interactions_of_today(user_id, device_id):
        try:
            user_timezone = users_service.get_timezone(user_id=user_id)
            if isinstance(user_timezone, dict):
                user_timezone = user_timezone.get("timezone", "UTC")
            if not user_timezone:
                user_timezone = "UTC"

            journal = journals_service.find_journal_of_today_by_id(user_id=user_id, user_timezone=user_timezone)
            if not journal:
                emit('interactions_of_today', {"error": "No journal found for today"})
                return

            interactions = interactions_service.list_interactions_by_journal(user_id=user_id, journal_id=journal.id)
            Logger.add_to_log("info", f"Interactions found: {interactions}")
            emit('interactions_of_today', interactions)
        except Exception as ex:
            Logger.add_to_log("error", f"Error en handle_get_interactions_of_today: {ex}")
            emit('interactions_of_today', {"error": INTERNAL_SERVER_ERROR})
    
    @socketio.on('get_all_journals')
    @SocketAuthMiddleware.require_auth
    def handle_get_journals(user_id, device_id):
        journals = journals_service.get_all(user_id=user_id)
        emit('all_journals', journals)

    @socketio.on('get_mood_evolution')
    @SocketAuthMiddleware.require_auth
    def handle_get_mood_evolution(user_id, device_id, range='week', week_offset=0):
        try:
            if not isinstance(user_id, (str, int ,uuid.UUID)):
                emit('mood_evolution_data', {
                    "success": False,
                    "error": "Invalid user id, must be a string, integer or UUID"
                })
                return
            
            result = mood_evolution_service.get_mood_evolution(user_id, range, week_offset)
            emit('mood_evolution_data', result)
        except Exception as ex:
            Logger.add_to_log("error", f"Error en handle_get_mood_evolution: {ex}")
            emit('mood_evolution_data', {
                "success": False,
                "error": INTERNAL_SERVER_ERROR
            })

    @socketio.on('get_word_cloud')
    @SocketAuthMiddleware.require_auth
    def handle_get_word_cloud(user_id, device_id):
        try:
            result = word_cloud_service.calculate_word_frequencies(user_id=user_id)
            emit('word_cloud_data', result)
        except Exception as ex:
            Logger.add_to_log("error", f"Error en handle_get_word_cloud: {ex}")
            emit('word_cloud_data', {
                "success": False,
                "error": INTERNAL_SERVER_ERROR
            })

    @socketio.on('get_mood_proportions')
    @SocketAuthMiddleware.require_auth
    def handle_get_mood_proportions(user_id, device_id):
        try:
            result = mood_pie_char_service.calculate_mood_proportions(user_id=user_id)
            emit('mood_proportions_data', result)
        except Exception as ex:
            Logger.add_to_log("error", f"Error en handle_get_mood_proportions: {ex}")
            emit('mood_proportions_data', {
                "success": False,
                "error": INTERNAL_SERVER_ERROR
            })