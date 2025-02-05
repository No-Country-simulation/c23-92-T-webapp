from datetime import datetime, timedelta
from src.repositories.InteractionsRepository import InteractionsRepository
from src.repositories.UserRepository import UserRepository  # Asumimos que tienes un repositorio para usuarios
from src.utils.Logger import Logger
import uuid
from pytz import timezone, UnknownTimeZoneError

class InteractionStatsService:
    def __init__(self):
        self.interactions_repository = InteractionsRepository()
        self.user_repository = UserRepository()

    def get_avg_interactions_per_week_in_current_month(self, user_id):
        """
        Calculate the average number of interactions per week in the current month,
        based on the user's timezone.

        Args:
            user_id (str, int, UUID): The ID of the user.

        Returns:
            dict: Success status and data with the average interactions per week.
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

            start_of_month = datetime(year, month, 1, tzinfo=user_timezone)
            if month == 12:
                next_month = datetime(year + 1, 1, 1, tzinfo=user_timezone)
            else:
                next_month = datetime(year, month + 1, 1, tzinfo=user_timezone)
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
                        "avg_interactions_per_week": 0,
                        "total_interactions": 0,
                        "weeks_with_interactions": 0,
                    },
                }

            weekly_counts = {}
            for interaction in interactions:
                week_number = interaction.date_interaction.astimezone(user_timezone).isocalendar()[1]
                if week_number not in weekly_counts:
                    weekly_counts[week_number] = 0
                weekly_counts[week_number] += 1

            total_interactions = sum(weekly_counts.values())
            weeks_with_interactions = len(weekly_counts)
            avg_interactions_per_week = total_interactions / weeks_with_interactions if weeks_with_interactions > 0 else 0

            return {
                "success": True,
                "data": {
                    "avg_interactions_per_week": round(avg_interactions_per_week, 2),
                    "total_interactions": total_interactions,
                    "weeks_with_interactions": weeks_with_interactions,
                },
            }

        except Exception as ex:
            Logger.add_to_log("error", f"Error en get_avg_interactions_per_week_in_current_month: {ex}")
            return {"success": False, "error": "Internal server error"}