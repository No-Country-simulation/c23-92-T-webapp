from src.utils.Logger import Logger
from dotenv import load_dotenv
from src.services.InteractionsService import InteractionsService
from openai import APIError

load_dotenv()

class OpenAIService:
    EMOTIONAL_STATES = {
        1: 'Feliz',
        2: 'Disgustado o Tenso',
        3: 'Triste',
        4: 'Enojado',
        5: 'Relajado o Cansado'
    }

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
        return self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Actúa como un consejero emocional y motivador. El usuario se siente {emotional_state}. Adapta tu respuesta considerando su estado emocional actual."},
                {"role": "user", "content": content},
            ],
            max_tokens=200,
            temperature=0.7,
            stream=True
        )

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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Genera un título corto y conciso (máximo 6 palabras) que resuma la siguiente interacción. Responde SOLO con el título, sin explicaciones adicionales."},
                {"role": "user", "content": f"Usuario ({emotional_state}): {content}\nRespuesta: {full_response}"},
            ],
            max_tokens=20,
            temperature=0.7
        )
        return str(title_response.choices[0].message.content).strip()

    def _process_response(self, response, socketio=None, event_name=None):
        """
        Process the OpenAI response and emit chunks if a socket is provided.
        
        Args:
            response (Generator): The OpenAI response stream.
            socket: The WebSocket connection (optional).
            event_name: The WebSocket event name (optional).
        
        Returns:
            str: The full response.
        """
        full_response = ""
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta:
                message_part = chunk.choices[0].delta.content
                if message_part:
                    full_response += message_part
                    if socketio and event_name:
                        socketio.emit(event_name, {
                            "type": "chunk",
                            "data": message_part,
                            "status": "streaming"
                        })
        if socketio and event_name:
            socketio.emit(event_name, {
                "type": "end",
                "data": full_response,
                "status": "complete"
            })
        return full_response

    def response(self, user_id, state, content, socketio=None, event_name=None):
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

            response = self._generate_openai_response(emotional_state, content)
            full_response = self._process_response(response, socketio, event_name)

            title = self._generate_title(emotional_state, content, full_response)
            self.interactions_service.create_interaction(user_id=user_id, title=title, state=state, content=content, response=full_response)
            
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