from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, URL, Optional

from models.profile import User


class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()
    remember_me = BooleanField('Keep me logged in')


class RegisterForm(FlaskForm):
    users_in_db = User.objects
    name_rule = Regexp('^[A-Za-z0-9_.]*$', 0, 'User names must have only letters, numbers dots or underscores')
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), name_rule])
    email = StringField('Email', validators=[DataRequired(), Length(1, 128), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Does not match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    register_submit = SubmitField('Register')

    def validate_username(self, field):
        if self.users_in_db.filter(username=field.data).count() > 0:
            raise ValidationError('Username already in use')

    def validate_email(self, field):
        if self.users_in_db.filter(email=field.data).count() > 0:
            raise ValidationError('Email already in registered')
