import traceback
from src.utils.Logger import Logger
from src.models.UserModel import User
from src.repositories.UserRepository import UserRepository


class AuthService():
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login_user(self, username, password):
        try:
            user = self.user_repository.get_user_by_username(username)
            if user and user.check_password(password):
                return user
            return None
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return None
        

    def register_user(self, username, email, password):
        try:
            if not username or not password:
                return {'error': 'Username and password are required'}
            
            if len(password) < 8:
                return {'error': 'Password must be at least 8 characters long'}

            if self.user_repository.get_user_by_username(username):
                return {'error': 'Username already exists'}
            
            if self.user_repository.get_user_by_email(email):
                return {'error': 'Email already exists'}
            
            user = User(username=username, email=email, password=password)
            self.user_repository.add(user)
            return {'success': True, 'message': 'User created'}
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return {'error': 'Internal server error'}
