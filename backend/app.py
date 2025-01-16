from flask import Flask, jsonify
from extensions import db, migrate
from src.routes.AuthRoutes import auth_routes
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)


    # Configurar SQLAlchemy con la URI de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Importar los modelos después de inicializar db
    app.register_blueprint(auth_routes, url_prefix='/api/auth')

    @app.get("/api")
    def home():
        return jsonify({
            "message": "Backend connected",
            "result": "Successfully"
        })
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)