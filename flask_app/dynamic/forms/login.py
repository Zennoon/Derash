#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    LoginForm - flask-wtf login form for the application
"""
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    """Login form for the application, inherits from FlaskForm"""
    email = StringField("Email", validators=[DataRequired(),
                                             Email()])
    password = StringField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
