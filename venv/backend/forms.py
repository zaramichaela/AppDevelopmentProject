from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,DecimalField,TextAreaField,IntegerField,DateField
from flask_wtf.file import FileField, FileRequired,FileAllowed
from wtforms.validators import DataRequired
from flask_uploads import UploadSet, IMAGES,configure_uploads
import os
import re

images = UploadSet('images', IMAGES)



#form to create a new sales item
class new_sales_item(FlaskForm):
    UID = StringField("Unique ID:", validators=[DataRequired()])
    name = StringField("Name: ", validators=[DataRequired()])
    description = TextAreaField("Description: ", validators=[DataRequired()])
    price = DecimalField("Price: ", validators=[DataRequired()])
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!'), FileRequired('File was empty!')])
    stocks = IntegerField("Stocks amount: ",  validators=[DataRequired()])
    submit = SubmitField()

#form to create a new sales item
class new_package(FlaskForm):
    UID = StringField("Unique ID:", validators=[DataRequired()])
    name = StringField("Name: ", validators=[DataRequired()])
    description = TextAreaField("Description: ", validators=[DataRequired()])
    price = DecimalField("Price: ", validators=[DataRequired()])
    expiry_duration = IntegerField("Valid for (days):", validators=[DataRequired()])
    sessions = IntegerField("Number of Sessions:", validators=[DataRequired()])
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!'), FileRequired('File was empty!')])
    submit = SubmitField()


#form to create a new sales item
class new_service(FlaskForm):
    UID = StringField("Unique ID:", validators=[DataRequired()])
    name = StringField("Name: ", validators=[DataRequired()])
    description = TextAreaField("Description: ", validators=[DataRequired()])
    price = DecimalField("Price: ", validators=[DataRequired()])
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!'), FileRequired('No file was selected')])
    submit = SubmitField()


#form to create a coupon item
class coupon_form(FlaskForm):
    UID = StringField("Unique ID: ", validators=[DataRequired()])
    coupon_code = StringField("Coupon Code: ", validators=[DataRequired()])
    percentage = IntegerField("Discount Percentage(%): ", validators=[DataRequired()])
    discountlimit = IntegerField("Maximum amount of discount($): ", validators=[DataRequired()])
    minimumspent = IntegerField("Minimum spending($): ", validators=[DataRequired()])
    expiredate = DateField("Expiry Date (DD/MM/YYYY): ", validators=[DataRequired()])
    submit = SubmitField()


