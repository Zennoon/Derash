#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    createDish - flask-wtf form for the application to create a new dish

    updateDish - flask-wtf form to update an existing dish
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (FileField, FloatField, StringField,
                     SubmitField, TextAreaField, ValidationError)
from wtforms.validators import DataRequired


class createDish(FlaskForm):
    """Form to register a new dish"""
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    ingredients = StringField("Ingredients", validators=[DataRequired()])
    price = FloatField("Price in ETB", validators=[DataRequired()])
    image_file = FileField("Upload an image", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Add dish")

    def validate_price(self, price):
        """Validates that the price is a valid float value"""
        if price.data <= 0:
            raise ValidationError("The price has to be greater that 0")


class updateDish(FlaskForm):
    """Form to update a dish"""
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    ingredients = StringField("Ingredients", validators=[DataRequired()])
    price = FloatField("Price in ETB", validators=[DataRequired()])
    image_file = FileField("Upload an image", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update dish")

    def validate_price(self, price):
        """Validates that the price is a valid float value"""
        if price.data <= 0:
            raise ValidationError("The price has to be greater that 0")