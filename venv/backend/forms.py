from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,DecimalField,TextAreaField,IntegerField,DateField, validators
from flask_wtf.file import FileField, FileRequired,FileAllowed
from wtforms.validators import DataRequired
from flask_uploads import UploadSet, IMAGES,configure_uploads
import os
import re

images = UploadSet('images', IMAGES)



#form to create a new sales item
class new_sales_item(FlaskForm):
    UID = StringField("Unique ID:", validators=[validators.Length(min=3, max=10),DataRequired()])
    name = StringField("Name: ", validators=[validators.Length(min=3, max=200) ,DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5, max=3000) ,DataRequired()])
    price = DecimalField("Price: ", validators=[DataRequired()])# Regexp(
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!'), FileRequired('File was empty!')])
    stocks = IntegerField("Stocks amount: ",  validators=[validators.NumberRange(min=1),DataRequired()])
    submit = SubmitField()

#form to create a new sales item
class new_package(FlaskForm):
    UID = StringField("Unique ID:", validators=[validators.Length(min=3, max=10),DataRequired()])
    name = StringField("Name: ", validators=[validators.Length(min=3, max=200),DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5) ,DataRequired()])
    price = DecimalField("Price: ", validators=[DataRequired()])
    expiry_duration = IntegerField("Valid for (days):", validators=[DataRequired()])
    sessions = IntegerField("Number of Sessions:", validators=[validators.NumberRange(min=1), DataRequired()])
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!'), FileRequired('File was empty!')])
    submit = SubmitField()


#form to create a new sales item
class new_service(FlaskForm):
    UID = StringField("Unique ID:", validators=[validators.Length(min=3, max=10),DataRequired()])
    name = StringField("Name: ", validators=[validators.Length(min=3, max=200),DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5, max=2000) ,DataRequired()])
    price = DecimalField("Price: ", validators=[validators.NumberRange(min=1),DataRequired()])
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!'), FileRequired('No file was selected')])
    submit = SubmitField()


#form to create a coupon item
class coupon_form(FlaskForm):
    UID = StringField("Unique ID: ", validators=[validators.Length(min=3, max=10),DataRequired()])
    coupon_code = StringField("Coupon Code: ", validators=[validators.Length(min=5, max=10),DataRequired()])
    percentage = IntegerField("Discount Percentage (%): ", validators=[validators.NumberRange(min=1, max=100),DataRequired()])
    discountlimit = DecimalField("Maximum amount of discount ($): ", validators=[validators.NumberRange(min=0.1),DataRequired()])
    minimumspent = IntegerField("Minimum spending ($): ", validators=[validators.NumberRange(min=1, max=2000),DataRequired()])
    expiredate = DateField("Expiry Date (DD/MM/YYYY): ", validators=[DataRequired()])
    submit = SubmitField()


