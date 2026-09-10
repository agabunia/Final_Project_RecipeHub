from flask import Blueprint, render_template, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Recipe
from app.recipes.forms import RecipeForm, DeleteForm
from app.utils.nutrition_api import get_nutrition_estimate, NutritionAPIError

recipes_bp = Blueprint('recipes', __name__)


@recipes_bp.route('/')
def list_recipes():
    recipes = Recipe.query.order_by(Recipe.date_added.desc()).all()
    return render_template('recipes/list.html', recipes=recipes)


@recipes_bp.route('/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    delete_form = DeleteForm()

    nutrition = None
    nutrition_error = None
    try:
        nutrition = get_nutrition_estimate(recipe.title)
    except NutritionAPIError as e:
        nutrition_error = str(e)

    return render_template(
        'recipes/detail.html',
        recipe=recipe,
        delete_form=delete_form,
        nutrition=nutrition,
        nutrition_error=nutrition_error
    )


@recipes_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            short_description=form.short_description.data,
            full_recipe=form.full_recipe.data,
            category=form.category.data,
            prep_time=form.prep_time.data,
            servings=form.servings.data,
            author=current_user
        )
        db.session.add(recipe)
        db.session.commit()

        current_app.logger.info(f'Recipe added: "{recipe.title}" by {current_user.email}')
        flash('Recipe added successfully!', 'success')
        return redirect(url_for('recipes.view_recipe', recipe_id=recipe.id))

    return render_template('recipes/form.html', form=form, title='Add Recipe')


@recipes_bp.route('/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.user_id != current_user.id:
        current_app.logger.warning(
            f'Unauthorized edit attempt on recipe {recipe.id} by {current_user.email}'
        )
        abort(403)

    form = RecipeForm(obj=recipe)
    if form.validate_on_submit():
        form.populate_obj(recipe)
        db.session.commit()

        current_app.logger.info(f'Recipe edited: "{recipe.title}" by {current_user.email}')
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('recipes.view_recipe', recipe_id=recipe.id))

    return render_template('recipes/form.html', form=form, title='Edit Recipe')


@recipes_bp.route('/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.user_id != current_user.id:
        current_app.logger.warning(
            f'Unauthorized delete attempt on recipe {recipe.id} by {current_user.email}'
        )
        abort(403)

    title = recipe.title
    db.session.delete(recipe)
    db.session.commit()

    current_app.logger.info(f'Recipe deleted: "{title}" by {current_user.email}')
    flash('Recipe deleted.', 'info')
    return redirect(url_for('recipes.list_recipes'))