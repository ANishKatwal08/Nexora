from flask import Blueprint
from app.controllers import authController

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return authController.home()

@auth_bp.route('/about')
def about():
    return authController.about()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return authController.register_user()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return authController.login_user()

@auth_bp.route('/logout')
def logout():
    return authController.logout_user()

@auth_bp.route('/dashboard')
def dashboard():
    return authController.dashboard()

@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    return authController.profile()