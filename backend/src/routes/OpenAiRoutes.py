from flask import Blueprint, request, jsonify
from src.services.OpenAiService import OpenAIService
from src.repositories.InteractionsRepository import InteractionsRepository
from openai import OpenAI
import os
from dotenv import load_dotenv

interactions_bp = Blueprint('interactions', __name__, url_prefix='/api/interactions')

load_dotenv()

client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

interactions_repository = InteractionsRepository()
openai_service = OpenAIService(interactions_repository, client)

@interactions_bp.route('/create', methods=['POST'])
def create_interaction():
    try:
        data = request.get_json()

        content = data.get("content")

        print(content)

        if not content:
            return jsonify({"error" : "Content is required"}), 400

        # falta agregar toda la logica del journal


        response = openai_service.response(content)

        if(response):
            return response, 201
        else:
            return jsonify({
                "error": "error"
            }), 400

    except Exception as ex:
        return jsonify({"error": f"error: {str(ex)}"}), 500
