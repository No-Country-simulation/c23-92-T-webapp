from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# url = os.getenv("DATABASE_URL")
# connection = psycopg2.connect(url)

# Configurar SQLAlchemy con la URI de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy y Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Importar los modelos después de inicializar db
from models import User


@app.get("/api")
def home():
    return jsonify({
        "message": "Backend connected",
        "result": "Successfully"
    })

if __name__ == "__main__":
    app.run(debug=True)