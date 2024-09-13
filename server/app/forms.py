# This represents a registration form for a Flask application.

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    """
    Registration form for a Flask application.
    """

    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=4, max=25, message='Username must be between 4 and 25 characters.')
    ])

    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Invalid email format.')
    ])

    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=6, max=35, message='Password must be between 6 and 35 characters.')
    ])