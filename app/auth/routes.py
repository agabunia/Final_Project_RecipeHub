from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User
from app.auth.forms import RegisterForm, LoginForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('recipes.list_recipes'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data.lower()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        current_app.logger.info(f'New user registered: {user.email}')
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('recipes.list_recipes'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            current_app.logger.info(f'Successful login: {user.email}')
            flash(f'Welcome back, {user.name}!', 'success')
            next_page = request_next_page()
            return redirect(next_page or url_for('recipes.list_recipes'))
        else:
            current_app.logger.warning(f'Failed login attempt for email: {form.email.data.lower()}')
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    current_app.logger.info(f'User logged out: {current_user.email}')
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('recipes.list_recipes'))


def request_next_page():
    from flask import request
    from urllib.parse import urlparse

    next_page = request.args.get('next')
    if next_page and urlparse(next_page).netloc == '':
        return next_page
    return None