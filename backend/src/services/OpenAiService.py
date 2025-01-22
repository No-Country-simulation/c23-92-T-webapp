from openai import OpenAI
from decouple import config
from src.utils.Logger import Logger
import os
from dotenv import load_dotenv
from src.models.Interactions import Interactions
from src.repositories.InteractionsRepository import InteractionsRepository


load_dotenv()

class OpenAIService:

    def __init__(self, interactions_repository: InteractionsRepository, client):
        self.interactions_repository = interactions_repository
        self.client = client

   
    def response(self, content, socket=None, event_name=None):
        try:
            if not content:
                return {"error": "Not content"}

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Actúa como un consejero emocional y motivador"},
                    {"role": "user", "content": content},
                ],
                max_tokens=200,
                temperature=0.7,
                stream=True 
            )

            full_response = ""
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta:
                    message_part = chunk.choices[0].delta.content
                    if message_part:
                        full_response += message_part
                        if socket and event_name:
                            socket.emit(event_name, {
                                "type": "chunk",
                                "data": message_part,
                                "status": "streaming"
                            })
            
            # Send completion message only after all chunks are processed
            if socket and event_name:
                socket.emit(event_name, {
                    "type": "end",
                    "data": full_response,
                    "status": "completed"
                })


            interaction = Interactions(content=content, response=full_response)
            self.interactions_repository.add(interaction)

            return {"response": full_response}

        except Exception as ex:
            Logger.add_to_log("error", f"Error al procesar la solicitud en OpenAIService: {ex}")
            if socket and event_name:
                socket.emit(event_name, {"error": f"Error: {str(ex)}"})
            raise ex