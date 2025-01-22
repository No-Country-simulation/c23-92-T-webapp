from flask import Blueprint, request, jsonify, render_template
from src.services.OpenAiService import OpenAIService
from src.repositories.JournalsRepository import JournalsRepository
from src.services.InteractionsService import InteractionsService
from src.services.JournalsService import JournalsService
from src.repositories.InteractionsRepository import InteractionsRepository
from src.middlewares.AuthMiddleware import AuthMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit
from extensions import socketio


load_dotenv()

interactions_bp = Blueprint('interactions', __name__, url_prefix='/api/interactions')

client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

journals_service = JournalsService()
interactions_service = InteractionsService()
openai_service = OpenAIService(client)

@interactions_bp.route('/createdebug', methods=['POST'])
def debug_headers():
    auth_header = request.headers.get('Authorization')
    print("Headers completos:", dict(request.headers))
    print("Authorization header:", auth_header)
    response = {
        "headers": dict(request.headers),
        "auth_header": auth_header,
        "method": request.method,
        "url": request.url,
        "json_body": request.get_json()
    }
    if auth_header:
        try:
            token = auth_header.split(' ')[1]
            print("Token extraído:", token)
            response["token"] = token
        except IndexError:
            print("Error al extraer el token del header")
            response["error"] = "Error al extraer el token del header"
    return jsonify(response)

@interactions_bp.route('/create', methods=['POST'])
@AuthMiddleware.require_auth
@AuthMiddleware.validate_request_data(["content", "state"])
def create_interaction(user_id):
    try:
        data = request.get_json()

        content = data.get("content")
        state = data.get("state")

        print(content, state)

        if not content:
            return jsonify({"error" : "Content is required"}), 400

        response = openai_service.response(user_id, state, content)

        if(response):
            return response, 201
        else:
            return jsonify({
                "error": "error"
            }), 400

    except Exception as ex:
        return jsonify({"error": f"error: {str(ex)}"}), 500
