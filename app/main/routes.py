# app/main/routes.py
from flask import Blueprint, render_template, redirect, url_for

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return redirect(url_for('recipes.list_recipes'))


@main_bp.route('/about')
def about():
    return render_template('main/about.html')