import re
from collections import Counter
from src.repositories.InteractionsRepository import InteractionsRepository
from src.utils.Logger import Logger
import spacy

nlp = spacy.load("es_core_news_sm")

POSITIVE_WORDS = {
    "feliz", "alegre", "contento", "gracias", "bien", "genial", "positivo",
    "excelente", "maravilloso", "increíble", "perfecto", "satisfecho", "orgulloso",
    "optimista", "esperanzado", "afortunado", "exitoso", "brillante", "divertido",
    "amable", "cariñoso", "generoso", "inspirador", "motivado", "entusiasmado",
    "relajado", "tranquilo", "pacífico", "seguro", "fuerte", "valiente",
    "agradecido", "comprendido", "apoyado", "animado", "encantado", "fascinado",
    "interesado", "curioso", "confiado", "respetuoso", "admirado", "celebrado",
    "triunfador", "prospero", "alentador", "radiante", "sorprendido", "conmovido"
}
NEGATIVE_WORDS = {
    "triste", "mal", "negativo", "problema", "difícil", "preocupado",
    "deprimido", "ansioso", "frustrado", "desesperado", "desgraciado",
    "culpable", "arrepentido", "desconfiado", "enojado", "irritado", "furioso",
    "resentido", "celoso", "envidioso", "inseguro", "vulnerable", "herido",
    "abandonado", "rechazado", "humillado", "ofendido", "traicionado", "engañoso",
    "confundido", "perdido", "desorientado", "abrumado", "estresado", "angustiado",
    "desalentado", "pesimista", "fracasado", "inútil", "desmotivado", "despreciado",
    "olvidado", "aislado", "indiferente", "desafiante", "amenazado", "aterrorizado",
    "paralizado", "indeciso", "incómodo", "insatisfecho", "descontento", "criticado",
    "acusado", "castigado", "atormentado", "desesperanzado", "fatalista"
}

class WordCloudService:
    def __init__(self):
        self.interactions_repository = InteractionsRepository()

    def preprocess_text(self, text):
        """
        Preprocess the text by tokenizing, cleaning, normalizing, and lemmatizing it.
        
        Args:
            text (str): The raw text.
        
        Returns:
            list: A list of cleaned and lemmatized words.
        """
        doc = nlp(text.lower())
        
        stopwords = {"el", "la", "los", "las", "de", "en", "y", "que", "es", "un", "una", "por", "con"}
        lemmas = [token.lemma_ for token in doc if token.is_alpha and token.lemma_ not in stopwords]
        
        return lemmas

    def calculate_word_frequencies(self, user_id):
        """
        Calculate word frequencies from all interactions for a specific user.
        
        Args:
            user_id (str): The ID of the user.
        
        Returns:
            dict: A dictionary with word frequencies and classification.
        """
        try:
            interactions = self.interactions_repository.get_all_interactions_by_user(user_id)
            
            global_word_counter = Counter()
            positive_words = Counter()
            negative_words = Counter()
            
            for interaction in interactions:
                words = self.preprocess_text(interaction.content)
                
                global_word_counter.update(words)
                
                for word in words:
                    if word in POSITIVE_WORDS:
                        positive_words[word] += 1
                    elif word in NEGATIVE_WORDS:
                        negative_words[word] += 1
            
            global_word_frequencies = dict(global_word_counter)
            positive_word_frequencies = dict(positive_words)
            negative_word_frequencies = dict(negative_words)
            
            return {
                "success": True,
                "global_word_frequencies": global_word_frequencies,
                "positive_words": positive_word_frequencies,
                "negative_words": negative_word_frequencies
            }
        except Exception as ex:
            Logger.add_to_log("error", f"Error en calculate_word_frequencies: {ex}")
            return {"success": False, "error": "Internal server error"}