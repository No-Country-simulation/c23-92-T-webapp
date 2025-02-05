from datetime import datetime, timedelta
from src.repositories.InteractionsRepository import InteractionsRepository
from src.repositories.UserRepository import UserRepository
from src.utils.Logger import Logger
import uuid
from pytz import timezone, UnknownTimeZoneError

class EmotionalProbabilityService:
    EMOTIONAL_STATES = {
        1: 'Feliz',
        2: 'Normal',
        3: 'Triste',
        4: 'Enojado',
    }

    def __init__(self):
        self.interactions_repository = InteractionsRepository()
        self.user_repository = UserRepository()

    def calculate_emotional_probabilities(self, user_id):
        """
        Calculate the probability of each emotional state in interactions for a given month.

        Args:
            user_id (str, int, UUID): The ID of the user.
            year (int): The year of the month to analyze.
            month (int): The month to analyze (1-12).

        Returns:
            dict: Success status and data with emotional probabilities.
        """
        try:
            if not isinstance(user_id, (str, int, uuid.UUID)):
                return {"success": False, "error": "Invalid user id, must be a string, integer or UUID"}
            
            user_timezone = self.user_repository.get_timezone(user_id=str(user_id))
            if not user_timezone:
                return {"success": False, "error": "User timezone not found"}

            try:
                user_timezone = timezone(user_timezone)
            except UnknownTimeZoneError:
                user_timezone = timezone("UTC")
                
            now_in_user_timezone = datetime.now(user_timezone)

            year = now_in_user_timezone.year
            month = now_in_user_timezone.month

            start_of_month = datetime(year, month, 1)
            if month == 12:
                next_month = datetime(year + 1, 1, 1)
            else:
                next_month = datetime(year, month + 1, 1)
            end_of_month = next_month - timedelta(days=1)

            interactions = self.interactions_repository.get_interactions_in_range(
                user_id=user_id,
                start_date=start_of_month,
                end_date=end_of_month
            )

            if not interactions:
                return {
                    "success": True,
                    "data": {
                        "emotional_probabilities": {state: 0 for state in self.EMOTIONAL_STATES.values()},
                        "total_interactions": 0,
                    },
                }

            emotional_counts = {state: 0 for state in self.EMOTIONAL_STATES.values()}
            total_interactions = len(interactions)

            for interaction in interactions:
                state = self.EMOTIONAL_STATES.get(interaction.state_interaction)
                if state:
                    emotional_counts[state] += 1

            emotional_probabilities = {
                state: round((count / total_interactions) * 100, 2) if total_interactions > 0 else 0
                for state, count in emotional_counts.items()
            }

            return {
                "success": True,
                "data": {
                    "emotional_probabilities": emotional_probabilities,
                    "total_interactions": total_interactions,
                },
            }

        except Exception as ex:
            Logger.add_to_log("error", f"Error en calculate_emotional_probabilities: {ex}")
            return {"success": False, "error": "Internal server error"}