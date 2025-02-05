from flask_socketio import emit, disconnect
from src.middlewares.SocketAuthMiddleware import SocketAuthMiddleware
from src.services.OpenAiService import OpenAIService
from src.utils.Logger import Logger
from openai import OpenAI
import os
from dotenv import load_dotenv
from flask import request


EVENT_INTERACTION_RESPONSE = "interaction_response"

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def register_interactions_events(socketio):

    openai_service = OpenAIService(client=client)

    @socketio.on('generate_interaction')
    @SocketAuthMiddleware.require_auth
    def handle_generate_interaction(data, user_id, device_id):
        try:
            content = data.get("content")
            state = data.get("state")

            if not content or not state:
                print(f"Missing content or state: content={content}, state={state}")
                emit(EVENT_INTERACTION_RESPONSE, {
                    "success": False,
                    "error": "Content and state are required",
                    "type": "error"
                })
                return
            
            print(f"User {user_id} requested interaction with data: {data}")
            
            Logger.add_to_log("info", f"User {user_id} requested interaction with data: {data}")
            
            response = openai_service.response(
                user_id=user_id,
                state=state,
                content=content,
            )

            emit(EVENT_INTERACTION_RESPONSE, {
                "type": "success",
                "title": response["title"],
                "response": response["response"],
                "success": response["success"]
            })

            print(f"Title: {response['title']}", f"Response: {response['response']}")

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            emit(EVENT_INTERACTION_RESPONSE, {
                "success": False,
                "error": "An error occurred while generating the interaction",
                "type": "error"
            })
            return