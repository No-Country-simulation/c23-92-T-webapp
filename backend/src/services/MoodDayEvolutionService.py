from datetime import datetime, timedelta, date
from decimal import Decimal
from src.repositories.InteractionsRepository import InteractionsRepository
from src.repositories.JournalsRepository import JournalsRepository
from src.repositories.UserRepository import UserRepository
from src.utils.Logger import Logger
import uuid
import pytz

class MoodDayEvolutionService:
    EMOTIONAL_STATES = {
        1: 'Feliz',
        2: 'Normal',
        3: 'Triste',
        4: 'Enojado',
    }

    def __init__(self):
        self.interactions_repository = InteractionsRepository()
        self.journals_repository = JournalsRepository()
        self.user_repository = UserRepository()

    def calculate_week_range(self, reference_date, week_offset=0):
        """
        Calculate the start and end dates of a week based on a reference date and week offset.
        
        Args:
            reference_date (datetime): The reference date (e.g., today).
            week_offset (int): Number of weeks to offset from the reference date.
        
        Returns:
            tuple: Start date and end date of the desired week.
        """
        start_of_week = reference_date - timedelta(days=reference_date.weekday())
        
        start_of_week += timedelta(weeks=week_offset)
        end_of_week = start_of_week + timedelta(days=6)
        
        return start_of_week.date(), end_of_week.date()

    def get_daily_mood_average_by_week(self, user_id, week_offset=0):
        """
        Calculate the average mood intensity for each day of the week.
        
        Args:
            user_id (str, int, UUID): The ID of the user.
            week_offset (int): Number of weeks to offset from the current week.
        
        Returns:
            dict: Success status and data with daily mood averages.
        """
        try:
            if not isinstance(user_id, (str, int, uuid.UUID)):
                return {"success": False, "error": "Invalid user id, must be a string, integer or UUID"}

            user_timezone = self.user_repository.get_timezone(user_id=str(user_id))
            try:
                tz = pytz.timezone(user_timezone)
            except pytz.UnknownTimeZoneError:
                tz = pytz.timezone("UTC")

            reference_date = datetime.now(tz=tz)

            start_date, end_date = self.calculate_week_range(reference_date, week_offset)

            Logger.add_to_log("info", f"Start date: {start_date}, End date: {end_date}")

            date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

            journals = self.journals_repository.get_journals_in_range(user_id, start_date, end_date)

            Logger.add_to_log("info", f"Journals found: {[journal.to_dict() for journal in journals]}")

            daily_averages = {d.isoformat(): [] for d in date_range}

            for journal in journals:
                journal_date = journal.date_journal.date().isoformat()
                if journal_date in daily_averages:
                    for interaction in journal.interactions:
                        intensity = float(interaction.mood_intensity) if isinstance(interaction.mood_intensity, Decimal) else interaction.mood_intensity
                        intensity = round(intensity, 2) if intensity is not None else 0
                        daily_averages[journal_date].append(intensity)

            formatted_data = []
            for date_key in sorted(daily_averages.keys()):
                intensities = daily_averages[date_key]
                average_intensity = sum(intensities) / len(intensities) if intensities else 0
                formatted_data.append({
                    "date": date_key,
                    "average_intensity": round(average_intensity, 2)
                })

            return {
                "success": True,
                "data": formatted_data,
                "week_offset": week_offset
            }

        except Exception as ex:
            Logger.add_to_log("error", f"Error en get_daily_mood_average_by_week: {ex}")
            return {"success": False, "error": "Internal server error"}