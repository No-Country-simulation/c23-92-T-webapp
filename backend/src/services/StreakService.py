from datetime import datetime, timedelta
from src.repositories.JournalsRepository import JournalsRepository
from src.repositories.UserRepository import UserRepository
from src.utils.Logger import Logger
import uuid
import pytz

class StreakService:
    def __init__(self):
        self.journals_repository = JournalsRepository()
        self.user_repository = UserRepository()

    def calculate_streaks(self, user_id):
        """
        Calculate the current streak and maximum streak of consecutive days for a user's journals.

        Args:
            user_id (str, int, UUID): The ID of the user.

        Returns:
            dict: Success status and data with current streak and maximum streak.
        """
        try:
            if not isinstance(user_id, (str, int, uuid.UUID)):
                return {"success": False, "error": "Invalid user id, must be a string, integer or UUID"}

            journals = self.journals_repository.find_all_by_user_id(user_id)
            if not journals:
                return {"success": True, "data": {"current_streak": 0, "max_streak": 0}}

            unique_dates = sorted(
                {journal.date_journal.date() for journal in journals}, reverse=True
            )

            timezone = self.user_repository.get_timezone(user_id=str(user_id))

            try:
                tz = pytz.timezone(timezone)
            except pytz.UnknownTimeZoneError:
                tz = pytz.timezone("UTC")

            current_streak = 0
            today = datetime.now(tz).date()
            for date in unique_dates:
                if date == today - timedelta(days=current_streak):
                    current_streak += 1
                else:
                    break

            max_streak = 0
            current_sequence = 0
            previous_date = None
            for date in unique_dates:
                if previous_date is None or date == previous_date - timedelta(days=1):
                    current_sequence += 1
                else:
                    max_streak = max(max_streak, current_sequence)
                    current_sequence = 1
                previous_date = date
            max_streak = max(max_streak, current_sequence)

            return {
                "success": True,
                "data": {
                    "current_streak": current_streak,
                    "max_streak": max_streak,
                },
            }

        except Exception as ex:
            Logger.add_to_log("error", f"Error en calculate_streaks: {ex}")
            return {"success": False, "error": "Internal server error"}