from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,DecimalField,TextAreaField,IntegerField,DateField, validators, PasswordField,SelectField
from flask_wtf.file import FileField, FileRequired,FileAllowed
from wtforms.validators import DataRequired,ValidationError
from flask_uploads import UploadSet, IMAGES,configure_uploads
from backend.settings import suppliercontroller, itemcontroller
import decimal
import re


images = UploadSet('images', IMAGES)


class BetterDecimalField(DecimalField):
    """
    Very similar to WTForms DecimalField, except with the option of rounding
    the data always.
    """
    def __init__(self, label=None, validators=None, places=2, rounding=None,
                 round_always=False, **kwargs):
        super(BetterDecimalField, self).__init__(
            label=label, validators=validators, places=places, rounding=
            rounding, **kwargs)
        self.round_always = round_always

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = decimal.Decimal(valuelist[0])
                if self.round_always and hasattr(self.data, 'quantize'):
                    exp = decimal.Decimal('.1') ** self.places
                    if self.rounding is None:
                        quantized = self.data.quantize(exp)
                    else:
                        quantized = self.data.quantize(
                            exp, rounding=self.rounding)
                    self.data = quantized
            except (decimal.InvalidOperation, ValueError):
                self.data = None
                raise ValueError(self.gettext('Not a valid decimal value'))

#form to create a new sales item
class new_sales_item(FlaskForm):
    UID = StringField("Unique ID:", validators=[validators.Length(min=3, max=10),DataRequired()])
    name = StringField("Name: ", validators=[validators.Length(min=3, max=200) ,DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5, max=3000) ,DataRequired()])
    price = BetterDecimalField("Price: ", validators=[DataRequired(message='You need to input a number!')])
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!'), FileRequired('File was empty!')])
    stocks = IntegerField("Stocks amount: ",  validators=[validators.NumberRange(min=1),DataRequired(message='You need to input a number!')])
    submit = SubmitField()

#form to create a new package item
class new_package(FlaskForm):
    UID = StringField("Unique ID:", validators=[validators.Length(min=3, max=10),DataRequired()])
    name = StringField("Name: ", validators=[validators.Length(min=3, max=200),DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5) ,DataRequired()])
    price = BetterDecimalField("Price: ", validators=[DataRequired(message='You need to input a number!')])
    expiry_duration = IntegerField("Valid for (days):", validators=[DataRequired(message='You need to input a number!')])
    sessions = IntegerField("Number of Sessions:", validators=[validators.NumberRange(min=1), DataRequired(message='You need to input a number!')])
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!'), FileRequired('File was empty!')])
    submit = SubmitField()


#form to create a new service item
class new_service(FlaskForm):
    UID = StringField("Unique ID:", validators=[validators.Length(min=3, max=10),DataRequired()])
    name = StringField("Name: ", validators=[validators.Length(min=3, max=200),DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5, max=2000) ,DataRequired()])
    price = BetterDecimalField("Price: ", validators=[validators.NumberRange(min=1),DataRequired(message='You need to input a number!')])
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!'), FileRequired('No file was selected')])
    submit = SubmitField()


#form to create a coupon item
class coupon_form(FlaskForm):
    UID = StringField("Unique ID: ", validators=[validators.Length(min=3, max=10),DataRequired()])
    couponcode = StringField("Coupon Code: ", validators=[validators.Length(min=5, max=10),DataRequired()])
    percentage = IntegerField("Discount Percentage (%): ", validators=[validators.NumberRange(min=1, max=100),DataRequired(message='You need to input a number!')])
    discountlimit = BetterDecimalField("Maximum amount of discount ($): ", validators=[validators.NumberRange(min=0.1),DataRequired(message='You need to input a number!')])
    minimumspent = IntegerField("Minimum spending ($): ", validators=[validators.NumberRange(min=1, max=2000),DataRequired(message='You need to input a number!')])
    expiredate = DateField("Expiry Date (DD/MM/YYYY): ",  format='%d/%m/%Y', validators=[DataRequired()])
    submit = SubmitField()


class edit_sales_item(FlaskForm):
    name = StringField("Name: ", validators=[validators.Length(min=3, max=200) ,DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5, max=3000) ,DataRequired()])
    price = BetterDecimalField("Price: ", validators=[DataRequired(message='You need to input a number!')])
    image = FileField("Image of product: ", validators=[FileAllowed(images,'Image only!')])
    stocks = IntegerField("Stocks amount: ",  validators=[validators.NumberRange(min=1), DataRequired(message='You need to input a number!')])
    submit = SubmitField()



class edit_package_form(FlaskForm):
    name = StringField("Name: ", validators=[validators.Length(min=3, max=200),DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5), DataRequired()])
    price = BetterDecimalField("Price: ", validators=[DataRequired(message='You need to input a number!')])
    expiry_duration = IntegerField("Valid for (days):", validators=[DataRequired(message='You need to input a number!')])
    sessions = IntegerField("Number of Sessions:", validators=[validators.NumberRange(min=1), DataRequired(message='You need to input a number!')])
    image = FileField("Image of product: ", validators=[FileAllowed(images, 'Image only!')])
    submit = SubmitField()



class edit_service_form(FlaskForm):
    name = StringField("Name: ", validators=[validators.Length(min=3, max=200),DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5, max=2000), DataRequired()])
    price = BetterDecimalField("Price: ", validators=[validators.NumberRange(min=1),DataRequired(message='You need to input a number!')])
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!')])
    submit = SubmitField()

class coupon_form(FlaskForm):
    couponcode = StringField("Coupon Code: ", validators=[validators.Length(min=5, max=10),DataRequired()])
    percentage = IntegerField("Discount Percentage (%): ", validators=[validators.NumberRange(min=1, max=100),DataRequired(message='You need to input a number!')])
    discountlimit = BetterDecimalField("Maximum amount of discount ($): ", validators=[validators.NumberRange(min=0.1),DataRequired(message='You need to input a number!')])
    minimumspent = IntegerField("Minimum spending ($): ", validators=[validators.NumberRange(min=1, max=2000),DataRequired(message='You need to input a number!')])
    expiredate = DateField("Expiry Date (DD/MM/YYYY): ",  format='%d/%m/%Y', validators=[DataRequired()])
    submit = SubmitField()

class edit_coupon_form(FlaskForm):
    percentage = IntegerField("Discount Percentage (%): ", validators=[validators.NumberRange(min=1, max=100),DataRequired(message='You need to input a number!')])
    discountlimit = BetterDecimalField("Maximum amount of discount ($): ", validators=[validators.NumberRange(min=0.1),DataRequired(message='You need to input a number!')])
    minimumspent = IntegerField("Minimum spending ($): ", validators=[validators.NumberRange(min=1, max=2000),DataRequired(message='You need to input a number!')])
    expiredate = DateField("Expiry Date (DD/MM/YYYY): ",  format='%d/%m/%Y', validators=[DataRequired()])
    submit = SubmitField()

class create_supplier(FlaskForm):
    UID = StringField("Unique ID:", validators=[validators.Length(min=3, max=10), DataRequired()])
    name = StringField("Supplier Name: ", validators=[validators.Length(min=3, max=200), DataRequired()])
    address = TextAreaField("Address: ", validators=[validators.Length(min=5, max=2000), DataRequired()])
    phone_num = StringField("Phone Number: ",validators=[validators.Length(max=8), validators.Regexp(r'^(?:\+?65)?[689]\d{7}$', message= 'Phone number needs to start with 6,8 or 9'),DataRequired(message='You need to input a number!')])
    product = StringField("Brand: ", validators=[DataRequired()])
    price = BetterDecimalField("Price: ", validators=[validators.NumberRange(min=1), DataRequired(message='You need to input a number!')])
    submit = SubmitField()


class buy_orders_supplier(FlaskForm):
    UID = StringField("Order UID:", validators=[validators.Length(min=3, max=10),DataRequired()])
    supplier = SelectField("Supplier")
    number = IntegerField("Number of orders:", validators=[validators.NumberRange(min=1), DataRequired(message='You need to input a number!')])
    submit = SubmitField()






class edit_admin_account(FlaskForm):
    old_password = PasswordField("Old Password:", validators=[validators.Length(min=8, max=16), DataRequired()])
    password = PasswordField("New Password:", validators=[validators.Length(min=8, max=16), DataRequired(), validators.EqualTo('cfm_password', message='Passwords must match')])
    cfm_password = PasswordField("Confirm Password:", validators=[validators.Length(min=8, max=16), DataRequired()])
    submit = SubmitField()



