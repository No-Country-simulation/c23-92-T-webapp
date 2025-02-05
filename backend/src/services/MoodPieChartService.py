from collections import defaultdict
from src.repositories.InteractionsRepository import InteractionsRepository
from src.utils.Logger import Logger
from datetime import datetime, timedelta
from src.repositories.UserRepository import UserRepository
import uuid
import pytz

class MoodPieChartService:
    EMOTIONAL_STATES = {
        1: 'Feliz',
        2: 'Normal',
        3: 'Triste',
        4: 'Enojado',
    }

    def __init__(self):
        self.interactions_repository = InteractionsRepository()
        self.user_repository = UserRepository()

    def calculate_mood_proportions(self, user_id):
        """
        Calculate the proportion of mood states for a specific user across all interactions.
        
        Args:
            user_id (str): The ID of the user.
        
        Returns:
            dict: A dictionary with mood proportions and additional details.
        """
        try:
            interactions = self.interactions_repository.get_all_interactions_by_user(user_id)
            
            mood_counter = defaultdict(int)
            total_interactions = len(interactions)
            
            for interaction in interactions:
                mood_counter[interaction.state_interaction] += 1
            
            mood_proportions = {}
            for state, count in mood_counter.items():
                mood_proportions[self.EMOTIONAL_STATES[state]] = round((count / total_interactions) * 100, 2)
            
            Logger.add_to_log("info", f"Mood proportions: {mood_proportions}")

            happiest_day = None
            saddest_day = None
            if interactions:
                happiest_day = max(
                    interactions,
                    key=lambda x: x.mood_intensity if x.state_interaction == 1 and x.mood_intensity is not None else 0
                ).date_interaction
                saddest_day = max(
                    interactions,
                    key=lambda x: x.mood_intensity if x.state_interaction == 3 and x.mood_intensity is not None else 0
                ).date_interaction
            
            Logger.add_to_log("info", f"Happiest day: {happiest_day}, saddest day: {saddest_day}")

            return {
                "success": True,
                "mood_proportions": mood_proportions,
                "total_interactions": total_interactions,
                "happiest_day": happiest_day.isoformat() if happiest_day else None,
                "saddest_day": saddest_day.isoformat() if saddest_day else None
            }
        except Exception as ex:
            Logger.add_to_log("error", f"Error en calculate_mood_proportions: {ex}")
            return {"success": False, "error": "Internal server error"}
        
    def calculate_mood_for_period(self, user_id, start_date, end_date):
        """
        Calculate mood proportions for a given period (weekly or monthly).

        Args:
            user_id (str, int, UUID): The ID of the user.
            start_date (datetime): Start date of the period.
            end_date (datetime): End date of the period.

        Returns:
            dict: Success status and data with mood proportions, total interactions, happiest day, and saddest day.
        """
        try:
            if not isinstance(user_id, (str, int, uuid.UUID)):
                return {"success": False, "error": "Invalid user id, must be a string, integer or UUID"}

            interactions = self.interactions_repository.get_interactions_in_range(user_id, start_date, end_date)
            if not interactions:
                return {
                    "success": True,
                    "mood_proportions": {state: 0 for state in self.EMOTIONAL_STATES.values()},
                    "total_interactions": 0,
                    "happiest_day": None,
                    "saddest_day": None,
                }

            mood_counts = {state: 0 for state in self.EMOTIONAL_STATES.values()}
            total_interactions = len(interactions)
            happiest_day = None
            saddest_day = None
            max_happiness = float('-inf')
            min_happiness = float('inf')

            for interaction in interactions:
                state = self.EMOTIONAL_STATES.get(interaction.state_interaction)
                if state:
                    mood_counts[state] += 1

                if interaction.mood_intensity is not None:
                    if interaction.mood_intensity > max_happiness:
                        max_happiness = interaction.mood_intensity
                        happiest_day = interaction.date_interaction
                    if interaction.mood_intensity < min_happiness:
                        min_happiness = interaction.mood_intensity
                        saddest_day = interaction.date_interaction

            mood_proportions = {
                state: (count / total_interactions) * 100 if total_interactions > 0 else 0
                for state, count in mood_counts.items()
            }

            return {
                "success": True,
                "mood_proportions": mood_proportions,
                "total_interactions": total_interactions,
                "happiest_day": happiest_day.isoformat() if happiest_day else None,
                "saddest_day": saddest_day.isoformat() if saddest_day else None,
            }

        except Exception as ex:
            Logger.add_to_log("error", f"Error en calculate_mood_for_period: {ex}")
            return {"success": False, "error": "Internal server error"}

    def calculate_weekly_mood(self, user_id, reference_date=None):
        """
        Calculate mood proportions for the week containing the reference date.

        Args:
            user_id (str, int, UUID): The ID of the user.
            reference_date (datetime): The reference date (default is today).

        Returns:
            dict: Success status and data with weekly mood proportions.
        """
        timezone = self.user_repository.get_timezone(user_id=str(user_id))

        try:
            tz = pytz.timezone(timezone)
        except Exception:
            tz = pytz.timezone("UTC")
        Logger.add_to_log("info", f"Timezone in calculate_weekly_mood: {timezone}")
        reference_date = reference_date or datetime.now(tz=tz)
        start_of_week = reference_date - timedelta(days=reference_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return self.calculate_mood_for_period(user_id, start_of_week.date(), end_of_week.date())

    def calculate_monthly_mood(self, user_id, reference_date=None):
        """
        Calculate mood proportions for the month containing the reference date.

        Args:
            user_id (str, int, UUID): The ID of the user.
            reference_date (datetime): The reference date (default is today).

        Returns:
            dict: Success status and data with monthly mood proportions.
        """
        timezone = self.user_repository.get_timezone(user_id=str(user_id))
        try:
            tz = pytz.timezone(timezone)
        except Exception:
            tz = pytz.timezone("UTC")
        Logger.add_to_log("info", f"Timezone in calculate_monthly_mood: {timezone}")
        reference_date = reference_date or datetime.now(tz=tz)
        start_of_month = reference_date.replace(day=1)
        next_month = start_of_month.replace(month=start_of_month.month % 12 + 1) if start_of_month.month < 12 else start_of_month.replace(year=start_of_month.year + 1, month=1)
        end_of_month = next_month - timedelta(days=1)
        return self.calculate_mood_for_period(user_id, start_of_month.date(), end_of_month.date())