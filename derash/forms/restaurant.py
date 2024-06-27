#!/usr/bin/python3
"""
Contains:
    Classes
    =======
    createRestaurant - flask-wtf form for the application to create a new restaurant

    updateRestaurant - flask-wtf form to update an existing restaurant
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import FileField, FloatField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class createRestaurant(FlaskForm):
    """Form to register a new restaurant"""
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    latitude = FloatField("Latitude", validators=[DataRequired()])
    longitude = FloatField("Longitude", validators=[DataRequired()])
    image_file = FileField("Upload an image", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Add Restaurant")


class updateRestaurant(FlaskForm):
    """Form to update a restaurant"""
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    latitude = FloatField("Latitude", validators=[DataRequired()])
    longitude = FloatField("Longitude", validators=[DataRequired()])
    image_file = FileField("Upload an image", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update Restaurant")
