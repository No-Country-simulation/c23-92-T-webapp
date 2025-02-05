from src.services.InteractionsService import InteractionsService
from src.services.JournalsService import JournalsService
from src.services.UserService import UserService
from src.services.MoodEvolutionService import MoodEvolutionService
from src.services.WordCloudService import WordCloudService
from src.services.MoodPieChartService import MoodPieChartService
from src.services.MoodDayEvolutionService import MoodDayEvolutionService
from src.services.StreakService import StreakService
from src.services.InteractionStatsService import InteractionStatsService
from src.services.EmotionalProbabilityService import EmotionalProbabilityService
from src.middlewares.SocketAuthMiddleware import SocketAuthMiddleware
from flask_socketio import emit
from src.utils.Logger import Logger
import uuid
from datetime import datetime

INTERNAL_SERVER_ERROR = "Internal server error"

def register_journal_events(socketio):
    interactions_service = InteractionsService()
    journals_service = JournalsService()
    users_service = UserService()
    mood_evolution_service = MoodEvolutionService()
    word_cloud_service = WordCloudService()
    mood_pie_char_service = MoodPieChartService()
    mood_day_evolution_service = MoodDayEvolutionService()
    streak_service = StreakService()
    interaction_stats_service = InteractionStatsService()
    emotional_probability_service = EmotionalProbabilityService()

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

    @socketio.on('get_mood_proportions_weekly')
    @SocketAuthMiddleware.require_auth
    def handle_get_mood_proportions_weekly(user_id, device_id):
        try:
            result = mood_pie_char_service.calculate_weekly_mood(user_id=user_id)
            emit('mood_proportions_weekly_data', result)
        except Exception as ex:
            Logger.add_to_log("error", f"Error en handle_get_mood_proportions_weekly: {ex}")
            emit('mood_proportions_weekly_data', {
                "success": False,
                "error": INTERNAL_SERVER_ERROR
            })

    @socketio.on('get_mood_proportions_monthly')
    @SocketAuthMiddleware.require_auth
    def handle_get_mood_proportions_monthly(user_id, device_id):
        try:
            result = mood_pie_char_service.calculate_monthly_mood(user_id=user_id)
            emit('mood_proportions_monthly_data', result)
        except Exception as ex:
            Logger.add_to_log("error", f"Error en handle_get_mood_proportions_monthly: {ex}")
            emit('mood_proportions_monthly_data', {
                "success": False,
                "error": INTERNAL_SERVER_ERROR
            })

    @socketio.on('get_mood_evolution_by_day')
    @SocketAuthMiddleware.require_auth
    def handle_get_evolution_by_day(user_id, device_id):
        try:
            result = mood_day_evolution_service.get_daily_mood_average_by_week(user_id=user_id)
            emit('mood_evolution_by_day_data', result)
        except Exception as ex:
            Logger.add_to_log("error", f"Error en hanle_get_evolution_by_day: {ex}")
            emit('mood_evolution_by_day_data', {
                "success": False,
                "error": INTERNAL_SERVER_ERROR
            })

    @socketio.on('get_journals_streak')
    @SocketAuthMiddleware.require_auth
    def handle_get_journals_streak(user_id, device_id):
        try:
            result = streak_service.calculate_streaks(user_id=user_id)
            emit('journals_streak_data', result)
        except Exception as ex:
            Logger.add_to_log("error", f"Error en handle_get_journals_streak: {ex}")
            emit('journals_streak_data', {
                "success": False,
                "error": INTERNAL_SERVER_ERROR
            })

    @socketio.on('get_avg_interactions_per_week_in_current_month')
    @SocketAuthMiddleware.require_auth
    def handle_get_avg_interactions_per_week_in_current_month(user_id, device_id):
        try:
            result = interaction_stats_service.get_avg_interactions_per_week_in_current_month(user_id=user_id)
            emit('avg_interactions_per_week_in_current_month_data', result)
        except Exception as ex:
            Logger.add_to_log("error", f"Error en handle_get_avg_interactions_per_week_in_current_month: {ex}")
            emit('avg_interactions_per_week_in_current_month_data', {
                "success": False,
                "error": INTERNAL_SERVER_ERROR
            })
    
    @socketio.on('get_emotional_probabilities')
    @SocketAuthMiddleware.require_auth
    def handle_get_emotional_probabilities(user_id, device_id):
        try:
            result = emotional_probability_service.calculate_emotional_probabilities(user_id=user_id)
            emit('emotional_probabilities_data', result)
        except Exception as ex:
            Logger.add_to_log("error", f"Error en handle_get_emotional_probabilities: {ex}")
            emit('emotional_probabilities_data', {
                "success": False,
                "error": INTERNAL_SERVER_ERROR
            })

    @socketio.on('get_journal_by_date')
    @SocketAuthMiddleware.require_auth
    def handle_get_journal_by_date(*args, **kwargs):
        try:
            user_id = kwargs.get("user_id")
            device_id = kwargs.get("device_id")

            if not user_id or not device_id:
                emit('journal_by_date_data', {
                    "success": False,
                    "error": "Authentication failed"
                })
                return

            if not args or not isinstance(args[0], dict):
                emit('journal_by_date_data', {
                    "success": False,
                    "error": "Missing or invalid data from client"
                })
                return

            data = args[0]
            target_date_str = None
            try:
                target_date_str = data.get("target_date")
                if not target_date_str:
                    raise ValueError("Missing or invalid target_date")

                target_date_obj = datetime.strptime(target_date_str, "%Y-%m-%d").date()

                result = journals_service.get_journal_for_day(
                    user_id=user_id,
                    target_date=target_date_obj
                )

                if not result["data"]:
                    emit('journal_by_date_data', {
                        "success": True,
                        "data": None,
                        "message": "No journal found for the given date"
                    })
                    return

                emit('journal_by_date_data', result)

            except ValueError as ve:
                Logger.add_to_log("error", f"ValueError en handle_get_journal_by_date: {ve}")
                emit('journal_by_date_data', {
                    "success": False,
                    "error": str(ve)
                })

            except Exception as ex:
                Logger.add_to_log("error", f"Error en handle_get_journal_by_date para user_id={user_id}, target_date={target_date_str}: {ex}")
                emit('journal_by_date_data', {
                    "success": False,
                    "error": "Internal server error"
                })

        except Exception as ex:
            Logger.add_to_log("error", f"Error inesperado en handle_get_journal_by_date: {ex}")
            emit('journal_by_date_data', {
                "success": False,
                "error": "Unexpected error"
            })