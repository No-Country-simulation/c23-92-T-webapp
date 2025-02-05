from datetime import datetime, timedelta, date
from decimal import Decimal
from src.repositories.InteractionsRepository import InteractionsRepository
from src.repositories.JournalsRepository import JournalsRepository
from src.repositories.UserRepository import UserRepository
from src.utils.Logger import Logger
import uuid
import pytz

class MoodEvolutionService:
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
        # Calcular el primer día de la semana actual
        start_of_week = reference_date - timedelta(days=reference_date.weekday())
        
        # Ajustar según el offset de semanas
        start_of_week += timedelta(weeks=week_offset)
        end_of_week = start_of_week + timedelta(days=6)
        
        Logger.add_to_log("info", f"Start of week: {start_of_week}, type: {type(start_of_week)}")
        Logger.add_to_log("info", f"End of week: {end_of_week}, type: {type(end_of_week)}")
        return start_of_week.date(), end_of_week.date()

    def get_mood_evolution(self, user_id, time_range='week', week_offset=0):
        try:
            if not isinstance(user_id, (str, int, uuid.UUID)):
                return {"success": False, "error": "Invalid user id, must be a string, integer or UUID"}

            # Obtener zona horaria del usuario
            user_timezone = self.user_repository.get_timezone(user_id=str(user_id))
            try:
                tz = pytz.timezone(user_timezone)
            except pytz.UnknownTimeZoneError:
                tz = pytz.timezone("UTC")

            # Fecha de referencia (hoy)
            reference_date = datetime.now(tz=tz)

            # Calcular el rango de fechas según el time_range y week_offset
            if time_range == 'week':
                start_date, end_date = self.calculate_week_range(reference_date, week_offset)
            else:
                # Para el rango mensual, mantener la lógica original
                start_date = reference_date.replace(day=1).date()
                end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

            Logger.add_to_log("info", f"Start date: {start_date}, End date: {end_date}")

            # Generar lista de fechas en el rango
            date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            Logger.add_to_log("info", f"Date range: {date_range}")

            # Obtener datos de la base de datos
            raw_data = self.interactions_repository.get_mood_evolution(user_id, start_date, end_date)
            Logger.add_to_log("info", f"Raw data: {raw_data}")

            # Estructurar los datos
            mood_data = {d.isoformat(): {state: None for state in self.EMOTIONAL_STATES} for d in date_range}
            Logger.add_to_log("info", f"Mood data: {mood_data}")
            for row in raw_data:
                date = row.date.isoformat()
                state = row.state_interaction
                avg_intensity = float(row.avg_intensity) if isinstance(row.avg_intensity, Decimal) else row.avg_intensity
                avg_intensity = round(avg_intensity, 2) if avg_intensity is not None else 0
                if date in mood_data:
                    mood_data[date][state] = avg_intensity

            # Formatear los datos para el gráfico
            formatted_data = []
            for date, states in sorted(mood_data.items()):
                entry = {"date": date}
                for state, label in self.EMOTIONAL_STATES.items():
                    entry[label] = states[state]
                formatted_data.append(entry)

            return {
                "success": True,
                "data": formatted_data,
                "time_range": time_range,
                "week_offset": week_offset
            }
        except Exception as ex:
            Logger.add_to_log("error", f"Error en get_mood_evolution: {ex}")
            return {"success": False, "error": "Internal server error"}