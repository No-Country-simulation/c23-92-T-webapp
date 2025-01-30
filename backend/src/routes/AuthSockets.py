from flask_socketio import emit, disconnect
from src.middlewares.SocketAuthMiddleware import SocketAuthMiddleware
from src.utils.Logger import Logger
from flask import request

def register_auth_events(socketio):
    @socketio.on('connect')
    @SocketAuthMiddleware.require_auth
    def handle_connect(*args, **kwargs):
        Logger.add_to_log("info", f"Usuario {kwargs['user_id']} conectado via WebSocket")
        emit('authentication_success', {"message": "Authenticated successfully"})