from src.utils.Logger import Logger
from dotenv import load_dotenv
from src.services.InteractionsService import InteractionsService


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


    def response(self, user_id, state, content):
        try:
            if not content:
                return {'success': False, 'error': 'Content is required'}
            
            emotional_state = self.EMOTIONAL_STATES.get(state, 'Desconocido')

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Actúa como un consejero emocional y motivador. El usuario se siente {emotional_state}. Adapta tu respuesta considerando su estado emocional actual."},
                    {"role": "user", "content": content},
                ],
                max_tokens=200,
                temperature=0.7
            )

            if not response:
                return {'success': False, 'error': 'No response from OpenAI'}
            
            response_received = str(response.choices[0].message.content)

            title_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Genera un título corto y conciso (máximo 6 palabras) que resuma la siguiente interacción. Responde SOLO con el título, sin explicaciones adicionales."},
                    {"role": "user", "content": f"Usuario ({emotional_state}): {content}\nRespuesta: {response_received}"},
                ],
                max_tokens=20,
                temperature=0.7
            )

            title = str(title_response.choices[0].message.content).strip()

            self.interactions_service.create_interaction(user_id=user_id, title=title, state=state, content=content, response=response_received)
            
            return {
                'success': True,
                "title": title,
                "response": response_received
            }
        except Exception as ex:
            Logger.add_to_log("error", f"Error al procesar la solicitud en OpenAIService: {ex}")
            return {'success': False, 'error': f"Error processing request with OpenAI: {ex}"}