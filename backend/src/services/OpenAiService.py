from openai import OpenAI
from decouple import config
from src.utils.Logger import Logger
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class OpenAIService:
    # Crear instancia del cliente OpenAI
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    @classmethod
    def response(cls, content):
        try:
            # Llamada al modelo de OpenAI usando la instancia del cliente
            response = cls.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Actúa como un consejero emocional y motivador."},
                    {"role": "user", "content": content},
                ],
                max_tokens=350,
                temperature=0.7
            )

            # Acceder al contenido del mensaje
            return response.choices[0].message.content

        except Exception as ex:
            # Manejo de errores con logging
            Logger.add_to_log("error", f"Error al procesar la solicitud en OpenAIService: {ex}")
            raise ex