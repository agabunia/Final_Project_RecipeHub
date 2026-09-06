# app/profile/routes.py
import os
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
import secrets
from PIL import Image
from app.extensions import db
from app.models import User, Recipe
from app.profile.forms import EditProfileForm

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/<int:user_id>')
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    recipes = user.recipes.order_by(Recipe.date_added.desc()).all()
    return render_template('profile/view.html', profile_user=user, recipes=recipes)


@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data.lower()

        if form.picture.data:
            filename = save_profile_picture(form.picture.data)
            current_user.profile_picture = filename

        db.session.commit()
        current_app.logger.info(f'Profile updated: {current_user.email}')
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.view_profile', user_id=current_user.id))

    return render_template('profile/edit.html', form=form)


# def save_profile_picture(file_storage):
    # ext = os.path.splitext(secure_filename(file_storage.filename))[1]
    # unique_name = f'{uuid.uuid4().hex}{ext}'
    # filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
    # file_storage.save(filepath)
    # return unique_name

def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_filename)
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_filename