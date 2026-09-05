# app/recipes/routes.py
from flask import Blueprint, redirect, url_for

recipes_bp = Blueprint('recipes', __name__)


@recipes_bp.route('/')
def list_recipes():
    return 'Recipes list placeholder'