#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    RequestResetForm - flask-wtf form for the application to
    request a password reset

    ResetPasswordForm - flask-wtf form for the application to
    reset a user's password
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from derash.models import db
from derash.models.user import User


class RequestResetForm(FlaskForm):
    """Form to request a password reset"""
    email = StringField("Email", validators=[DataRequired(),
                                             Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        """Checks that the email is in the database"""
        user = db.filter_by_attr(User, "email", email.data)
        if len(user) == 0:
            raise ValidationError("There is no account with that email. Please register first.")
        

class ResetPasswordForm(FlaskForm):
    """Form to reset password"""
    password = StringField("New password", validators=[DataRequired()])
    confirm_password = StringField("Confirm password", validators=[DataRequired(),
                                                                   EqualTo("password")])
    submit = SubmitField("Reset Password")
