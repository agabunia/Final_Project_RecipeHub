from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_login import current_user
from app.models import User


class EditProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only (jpg, jpeg, png).')
    ])
    submit = SubmitField('Save Changes')

    def validate_email(self, field):
        existing = User.query.filter_by(email=field.data.lower()).first()
        if existing and existing.id != current_user.id:
            raise ValidationError('That email is already in use by another account.')