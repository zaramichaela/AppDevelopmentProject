from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,DecimalField,TextAreaField,IntegerField,DateField
from flask_wtf.file import FileField, FileRequired,FileAllowed
from wtforms.validators import DataRequired
from flask_uploads import UploadSet, IMAGES,configure_uploads
import os

images = UploadSet('images', IMAGES)

#form to create a new sales item
class create_sales_item(FlaskForm):
    UID = StringField("UniqueID:", validators=[DataRequired()])
    name = StringField("Name: ", validators=[DataRequired()])
    description = TextAreaField("Description: ", validators=[DataRequired()])
    price = DecimalField("Price: ", validators=[DataRequired()])
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!'), FileRequired('File was empty!')])
    stocks = IntegerField("Stocks amount: ",  validators=[DataRequired()])
    submit = SubmitField()

#form to create a coupon item
class coupon_form(FlaskForm):
    UID = StringField("UniqueID: ", validators=[DataRequired()])
    coupon_code = StringField("Coupon Code: ", validators=[DataRequired()])
    percentage = IntegerField("Discount Percentage(%): ", validators=[DataRequired()])
    discountlimit = IntegerField("Maximum amount of discount($): ", validators=[DataRequired()])
    minimumspent = IntegerField("minimum spending($): ", validators=[DataRequired()])
    expiredate = DateField("Expiry Date: ", validators=[DataRequired()])
    submit = SubmitField()


