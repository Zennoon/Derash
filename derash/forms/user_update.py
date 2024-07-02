#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    UpdateAccountForm - flask-wtf form for the application to update account of customer, or owner

    UpdateAccountDriverForm - flask-wtf form for the application to update account of driver
"""
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length

from derash.models import db
from derash.models.user import User


class UpdateAccountForm(FlaskForm):
    """Form to update account info of customers, and owners"""
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(),
                                             Email()])
    phone_num = StringField("Phone Number", validators=[DataRequired(),
                                                        Length(10, 10)])
    image_file = FileField("Upload an image", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Save")

    def validate_email(self, email):
        """Checks if email is already registered under another user"""
        user = db.filter_by_attr(User, "email", email.data)
        if len(user) != 0 and user[0].id != current_user.id:
            raise ValidationError("The email is already registered, please use another email")
        

class UpdateDriverAccountForm(UpdateAccountForm):
    """Form to update account info of drivers"""
    license_num = StringField("License Plate Number", validators=[DataRequired()])

