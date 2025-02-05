from flask import Blueprint, render_template
from src.middlewares.AuthMiddleware import AuthMiddleware

 
test_routes = Blueprint('test_routes', __name__, template_folder='../templates')


@test_routes.route('/login')
@AuthMiddleware.reject_authenticated_json
def login():
    return render_template('login.html')

@test_routes.route('/register')
@AuthMiddleware.reject_authenticated_json
def register():
    return render_template('register.html')

@test_routes.route('/testSocket')
def home(**kwargs):
    print("Rendering testSocket.html")
    return render_template('testSocket.html')
