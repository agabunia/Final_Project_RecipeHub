from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

CATEGORY_CHOICES = [
    ('Breakfast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner'),
    ('Dessert', 'Dessert'),
    ('Vegan', 'Vegan'),
    ('Snack', 'Snack'),
]


class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=150)])
    short_description = StringField(
        'Short Description', validators=[DataRequired(), Length(max=300)]
    )
    full_recipe = TextAreaField('Full Recipe', validators=[DataRequired()])
    category = SelectField('Category', choices=CATEGORY_CHOICES, validators=[DataRequired()])
    prep_time = IntegerField(
        'Preparation Time (minutes)', validators=[DataRequired(), NumberRange(min=1, max=1000)]
    )
    servings = IntegerField(
        'Servings', validators=[DataRequired(), NumberRange(min=1, max=100)]
    )
    submit = SubmitField('Save Recipe')


class DeleteForm(FlaskForm):
    pass