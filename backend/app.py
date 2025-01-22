from flask import Flask, jsonify, render_template
from extensions import db, migrate, socketio
from src.routes.AuthRoutes import auth_routes
from src.routes.OpenAiRoutes import interactions_bp
from dotenv import load_dotenv
import os
from flask_socketio import SocketIO


load_dotenv()

def create_app():
    app = Flask(__name__)

    # username = os.getenv("DB_USERNAME")
    # password = os.getenv("DB_PASSWORD")
    # host = os.getenv("DB_HOST")
    # port = os.getenv("DB_PORT")
    # database = os.getenv("DB_NAME")
    # sslmode = "require"
    # connection_string = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}?sslmode={sslmode}"


    
    app.config['SQLALCHEMY_DATABASE_URI'] =  os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    
    app.register_blueprint(auth_routes, url_prefix='/api/auth')
    app.register_blueprint(interactions_bp)

    @app.get("/")
    def home():
        return "hello"

    return app

app = create_app()

if __name__ == "__main__":
    app = create_app()
    # Ejecutar el servidor con SocketIO
    socketio.run(app, debug=True)