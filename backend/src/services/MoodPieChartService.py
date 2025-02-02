from collections import defaultdict
from src.repositories.InteractionsRepository import InteractionsRepository
from src.utils.Logger import Logger

class MoodPieChartService:
    EMOTIONAL_STATES = {
        1: 'Feliz',
        2: 'Disgustado o Tenso',
        3: 'Triste',
        4: 'Enojado',
        5: 'Relajado o Cansado'
    }

    def __init__(self):
        self.interactions_repository = InteractionsRepository()

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