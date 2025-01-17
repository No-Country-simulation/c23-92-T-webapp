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

   
    def response(self, content):
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
                temperature=0.7
            )


            if not response:
                return {"error": "Not reponse"}
            
            responseReceived = str(response.choices[0].message.content)

            interaction = Interactions(content=content, response=responseReceived)

            self.interactions_repository.add(interaction)

            return responseReceived

        except Exception as ex:
           
            Logger.add_to_log("error", f"Error al procesar la solicitud en OpenAIService: {ex}")
            raise ex