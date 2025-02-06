import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify
from src.routes.AuthRoutes import auth_routes
from src.routes.OpenAiRoutes import interactions_bp
from src.routes.TokenRoutes import token_routes
from src.routes.TestRoutes import test_routes
from src.routes.AuthSockets import register_auth_events
from src.routes.OpenAiSockets import register_interactions_events
from src.routes.JournalSockets import register_journal_events
from dotenv import load_dotenv
from extensions import db, socketio
from flask_cors import CORS
import os

# Importar todos los modelos
from src.models.Interactions import Interactions
from src.models.User import User
from src.models.Journal import Journal


load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(
        app,
        resources={r"/*": {
            "origins": ["http://localhost:3000", "http://192.168.18.118:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "supports_credentials": True,
            "allow_headers": ["Authorization", "Content-Type"],
        }},
    )

    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    sslmode = "require"

    connection_string = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}?sslmode={sslmode}"

    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    db.init_app(app)

    socketio.init_app(app, cors_allowed_origins="*", cors_credentials=True)

    with app.app_context():
        print("Verificando la conexión a la base de datos y modelos registrados...")

        try:
            print("\nModelos registrados en SQLAlchemy:")
            for clase in [User, Journal, Interactions]:
                print(f"- {clase.__name__}: {clase.__tablename__}")

            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            print("\nTablas existentes en la base de datos:")
            for table in existing_tables:
                print(f"- {table}")

            if not existing_tables:
                print("\nNo se encontraron tablas. Procediendo a la creación...")
                db.create_all()
                db.session.commit()
                
                inspector = db.inspect(db.engine)
                created_tables = inspector.get_table_names()
                print("\nTablas creadas:")
                for table in created_tables:
                    print(f"- {table}")
                    columns = inspector.get_columns(table)
                    for column in columns:
                        print(f"  - {column['name']}: {column['type']}")
            else:
                print("\nTablas existentes:")
                for table in existing_tables:
                    print(f"- {table}")
                    columns = inspector.get_columns(table)
                    for column in columns:
                        print(f"  - {column['name']}: {column['type']}")
            
        except Exception as e:
            print(f"Error al verificar/crear las tablas: {str(e)}")
            db.session.rollback()
            raise

    app.register_blueprint(auth_routes, url_prefix='/api/auth')
    app.register_blueprint(interactions_bp)
    app.register_blueprint(token_routes, url_prefix='/api/token')
    app.register_blueprint(test_routes)
    register_auth_events(socketio)
    register_interactions_events(socketio)
    register_journal_events(socketio)

    @app.route("/api", methods=["GET"])
    def home():
        return jsonify({
            "message": "Backend connected",
            "result": "Successfully"
        })

    return app, socketio

if __name__ == "__main__":
    app, socketio = create_app()
    socketio.run(app, host="0.0.0.0", port=5000, debug=False, allow_unsafe_werkzeug=True)
