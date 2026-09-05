# app/profile/routes.py
from flask import Blueprint

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/')
def view_profile():
    return 'Profile placeholder'