from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO

socketio = SocketIO()
db = SQLAlchemy()
