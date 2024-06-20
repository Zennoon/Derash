#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    RegisterCustomerForm - flask-wtf form for the application
    to register a new customer

    RegisterOwnerForm - flask-wtf form for the application to
    register a new owner

    RegisterDriverForm - flask-wtf form for the application to
    register a new driver
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from derash.models import db
from derash.models.user import User


class RegisterCustomerForm(FlaskForm):
    """Form to register a new customer"""
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(),
                                             Email()])
    phone_num = StringField("Phone Number", validators=[DataRequired(),
                                                        Length(10, 10)])
    password = StringField("Password", validators=[DataRequired()])
    confirm_password = StringField("Confirm Password", validators=[DataRequired(),
                                                                   EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        """Checks if email is already registered"""
        user = db.filter_by_attr(User, "email", email.data)
        if len(user) != 0:
            raise ValidationError("The email is already registered, please use another email")


class RegisterOwnerForm(RegisterCustomerForm):
    """Form to register a new owner"""
    pass


class RegisterDriverForm(RegisterCustomerForm):
    """Form to register a new driver"""
    license_num = StringField("License Plate Number",
                              validators=[DataRequired()])
