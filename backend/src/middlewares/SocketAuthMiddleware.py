from functools import wraps
from extensions import socketio
from src.utils.Security import Security
from src.utils.Logger import Logger
from flask import request
from flask_socketio import disconnect
import jwt

class SocketAuthMiddleware:
    @staticmethod
    def require_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            sid = getattr(request, 'sid', None)  # Obtener sid de manera segura
            try:
                Logger.add_to_log("info", "Iniciando autenticación WebSocket")

                if not sid:
                    Logger.add_to_log("error", "No se pudo obtener el sid del request")
                    socketio.emit('authentication_error', {"message": "Internal server error"}, room=sid)
                    return

                token_result = Security.get_websocket_cookie('token', max_age=7200)
                device_id_result = Security.get_websocket_cookie('device_id', max_age=30 * 24 * 60 * 60)  # 30 days

                Logger.add_to_log("info", f"Token result: {token_result}")
                Logger.add_to_log("info", f"Device ID result: {device_id_result}")

                if not token_result.get('success') or not device_id_result.get('success'):
                    Logger.add_to_log("info", "No token or device_id provided")
                    socketio.emit('authentication_error', {"message": "No token or device_id provided"}, room=sid)
                    disconnect(sid=sid)
                    return

                access_token = token_result['value']
                device_id = device_id_result['value']

                try:
                    payload = jwt.decode(
                        access_token, 
                        Security.secret, 
                        algorithms=["HS256"],
                        options={
                            'verify_signature': True,
                            'require_exp': True,
                            'verify_exp': True,
                            'verify_iat': True
                        }
                    )
                except jwt.ExpiredSignatureError:
                    Logger.add_to_log("info", "Token has expired")
                    socketio.emit('token_expired', {"message": "Token has expired, please refresh it"}, room=sid)
                    disconnect(sid=sid)
                    return
                except jwt.InvalidTokenError as e:
                    Logger.add_to_log("info", f"Invalid token: {str(e)}")
                    socketio.emit('authentication_error', {"message": "Invalid token"}, room=sid)
                    disconnect(sid=sid)
                    return

                if not Security.is_valid_payload(payload):
                    Logger.add_to_log("info", "Invalid token payload")
                    socketio.emit('authentication_error', {"message": "Invalid token payload"}, room=sid)
                    disconnect(sid=sid)
                    return

                if payload['device_id'] != device_id:
                    Logger.add_to_log("info", "Device ID mismatch")
                    socketio.emit('authentication_error', {"message": "Invalid device"}, room=sid)
                    disconnect(sid=sid)
                    return

                if not Security.validate_device(payload['id'], payload['device_id']):
                    Logger.add_to_log("info", f"Unauthorized device for user: {payload.get('id')}")
                    socketio.emit('authentication_error', {"message": "Unauthorized device"}, room=sid)
                    disconnect(sid=sid)
                    return

                Logger.add_to_log("info", f"Authenticated user: {payload.get('id')}")

                kwargs['user_id'] = payload.get('id')
                kwargs['device_id'] = payload.get('device_id')

                return f(*args, **kwargs)

            except Exception as ex:
                Logger.add_to_log("error", f"WebSocket authentication error: {str(ex)}")
                if sid:  # Verificar si sid tiene un valor antes de usarla
                    socketio.emit('authentication_error', {"message": "Unexpected error during authentication"}, room=sid)
                    disconnect(sid=sid)
                return

        return decorated