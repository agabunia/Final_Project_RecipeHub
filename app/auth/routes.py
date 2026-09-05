# app/auth/routes.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    return 'Login page placeholder'


@auth_bp.route('/register')
def register():
    return 'Register page placeholder'


@auth_bp.route('/logout')
def logout():
    return 'Logout placeholder'