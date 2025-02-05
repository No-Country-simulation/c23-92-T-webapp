from src.utils.Logger import Logger
from dotenv import load_dotenv
from src.services.InteractionsService import InteractionsService
from openai import APIError
import re

load_dotenv()

class OpenAIService:
    EMOTIONAL_STATES = {
        1: 'Feliz',
        2: 'Normal',
        3: 'Triste',
        4: 'Enojado',
    }

    CLIENT_NAME = "gpt-3.5-turbo"

    def __init__(self, client):
        self.interactions_service = InteractionsService()
        self.client = client

    def _generate_openai_response(self, emotional_state, content):
        """
        Generate a response using OpenAI.
        
        Args:
            emotional_state (str): The emotional state of the user.
            content (str): The user's input.
        
        Returns:
            Generator: The OpenAI response stream.
        """
        response = self.client.chat.completions.create(
            model=self.CLIENT_NAME,
            messages=[
                {"role": "system", "content": (
                    f"Eres un consejero emocional y motivador. El usuario se siente {emotional_state}. "
                    "Tu tarea es adaptar tus respuestas considerando su estado emocional actual. "
                    "Sé empático, claro y breve. Si el mensaje del usuario no tiene sentido o es incomprensible, "
                    "responde con un mensaje amigable indicando que no entendiste lo que dijo. "
                    "Si el usuario pregunta algo fuera del ámbito del diario emocional, redirígelo amablemente "
                    "al propósito de esta conversación, enfocándote en sus emociones y experiencias."
                )},
                {"role": "user", "content": content},
            ],
            max_tokens=200,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()
    
    def _is_incomprehensible(self, content):
        """
        Detect if the content is incomprehensible (random characters without meaning).

        Args:
            content (str): The user's input.

        Returns:
            bool: True if the content is likely incomprehensible, False otherwise.
        """
        # Patrón para detectar cadenas aleatorias (sin palabras ni estructura clara)
        random_pattern = re.compile(r'^[a-zA-Z]{10,}$')  # Ejemplo: más de 10 letras consecutivas sin espacios
        if random_pattern.match(content):
            return True

        vowels = set("aeiouáéíóú")
        if not any(char.lower() in vowels for char in content):
            return True

        return False

    def _calculate_mood_intensity(self, emotional_state, content):
        """
        Calculate the mood intensity based on the user's input and emotional state.
        
        Args:
            emotional_state (str): The emotional state of the user.
            content (str): The user's input.
        
        Returns:
            int: The calculated mood intensity (0-10).
        """

        if self._is_incomprehensible(content):
            return 1  # Asignar una intensidad emocional baja para mensajes incomprensibles

        mood_response = self.client.chat.completions.create(
            model=self.CLIENT_NAME,
            messages=[
                {"role": "system", "content": "Evalúa la intensidad del estado emocional del usuario basado en su mensaje. Responde con un número entero entre 0 y 10, donde 0 es la intensidad mínima y 10 es la máxima."},
                {"role": "user", "content": f"Estado emocional: {emotional_state}\nMensaje del usuario: {content}"},
            ],
            max_tokens=5,
            temperature=0.5
        )
        
        mood_intensity = mood_response.choices[0].message.content.strip()
        try:
            mood_intensity = int(mood_intensity)
            return min(max(mood_intensity, 0), 10)  # Asegurar que esté en el rango [0, 10]
        except ValueError:
            return 5 

    def _generate_title(self, emotional_state, content, full_response):
        """
        Generate a title for the interaction.
        
        Args:
            emotional_state (str): The emotional state of the user.
            content (str): The user's input.
            full_response (str): The full response from OpenAI.
        
        Returns:
            str: The generated title.
        """
        title_response = self.client.chat.completions.create(
            model=self.CLIENT_NAME,
            messages=[
                {"role": "system", "content": "Genera un título corto y conciso (máximo 6 palabras) que resuma la siguiente interacción. Responde SOLO con el título, sin explicaciones adicionales."},
                {"role": "user", "content": f"Usuario ({emotional_state}): {content}\nRespuesta: {full_response}"},
            ],
            max_tokens=20,
            temperature=0.7
        )
        return str(title_response.choices[0].message.content).strip()

    def response(self, user_id, state, content):
        """
        Generate a response using OpenAI and save the interaction.
        
        Args:
            user_id (str): The ID of the user.
            state (int): The emotional state of the user.
            content (str): The user's input.
            socket: The WebSocket connection (optional).
            event_name: The WebSocket event name (optional).
        
        Returns:
            dict: A dictionary with the success status, title, and response.
        """
        try:
            if not content:
                return {'success': False, 'error': 'Content is required'}
            
            if state not in self.EMOTIONAL_STATES:
                return {'success': False, 'error': 'Invalid emotional state'}
            
            emotional_state = self.EMOTIONAL_STATES[state]
            mood_intensity = self._calculate_mood_intensity(emotional_state, content)
            full_response = self._generate_openai_response(emotional_state, content)

            title = self._generate_title(emotional_state, content, full_response)
            self.interactions_service.create_interaction(user_id=user_id, title=title, state=state, content=content, response=full_response, mood_intensity=mood_intensity)
            
            return {
                'success': True,
                "title": title,
                "response": full_response
            }
        except APIError as ex:
            Logger.add_to_log("error", f"OpenAI API error: {str(ex)}")
            return {'success': False, 'error': 'OpenAI service is unavailable'}
        except Exception as ex:
            Logger.add_to_log("error", f"Unexpected error: {str(ex)}")
            return {'success': False, 'error': 'Internal server error'}