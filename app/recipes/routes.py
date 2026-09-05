# app/recipes/routes.py
from flask import Blueprint

recipes_bp = Blueprint('recipes', __name__)


@recipes_bp.route('/')
def list_recipes():
    return 'Recipes list placeholder'


@recipes_bp.route('/add')
def add_recipe():
    return 'Add recipe placeholder'