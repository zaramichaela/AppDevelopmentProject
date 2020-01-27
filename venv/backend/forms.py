from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,DecimalField,TextAreaField,IntegerField,DateField, validators, PasswordField,SelectField
from flask_wtf.file import FileField, FileRequired,FileAllowed
from wtforms.validators import DataRequired,ValidationError,input_required
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
    category = StringField("Category: ", validators=[validators.Length(min=3, max=30) ,DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5, max=3000) ,DataRequired()])
    price = BetterDecimalField("Actual Price: ", validators=[DataRequired(message='You need to input a number!')])
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!'), FileRequired('File was empty!')])
    stocks = IntegerField("Stocks amount: ",  validators=[validators.NumberRange(min=1),DataRequired(message='You need to input a number!')])
    discount = IntegerField("Discount(%): ", validators=[validators.NumberRange(min=0, max=100), validators.input_required()])
    submit = SubmitField()

#form to create a new package item
class new_package(FlaskForm):
    UID = StringField("Unique ID:", validators=[validators.Length(min=3, max=10),DataRequired()])
    name = StringField("Name: ", validators=[validators.Length(min=3, max=200),DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5) ,DataRequired()])
    price = BetterDecimalField("Actual Price: ", validators=[DataRequired(message='You need to input a number!')])
    expiry_duration = IntegerField("Valid for (days):", validators=[DataRequired(message='You need to input a number!')])
    sessions = IntegerField("Number of Sessions:", validators=[validators.NumberRange(min=1), DataRequired(message='You need to input a number!')])
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!'), FileRequired('File was empty!')])
    discount = IntegerField("Discount(%): ", validators=[validators.NumberRange(min=0, max=100), validators.input_required()])
    submit = SubmitField()


#form to create a new service item
class new_service(FlaskForm):
    UID = StringField("Unique ID:", validators=[validators.Length(min=3, max=10),DataRequired()])
    name = StringField("Name: ", validators=[validators.Length(min=3, max=200),DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5, max=2000) ,DataRequired()])
    price = BetterDecimalField("Actual Price: ", validators=[validators.NumberRange(min=1),DataRequired(message='You need to input a number!')])
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!'), FileRequired('No file was selected')])
    discount = IntegerField("Discount(%): ", validators=[validators.NumberRange(min=0, max=100), validators.input_required()])
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
    category = StringField("Category: ", validators=[validators.Length(min=3, max=30) ,DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5, max=3000) ,DataRequired()])
    price = BetterDecimalField("Actual Price: ", validators=[DataRequired(message='You need to input a number!')])
    image = FileField("Image of product: ", validators=[FileAllowed(images,'Image only!')])
    stocks = IntegerField("Stocks amount: ",  validators=[validators.NumberRange(min=1), DataRequired(message='You need to input a number!')])
    discount = IntegerField("Discount(%): ", validators=[validators.NumberRange(min=0, max=100), validators.input_required()])
    submit = SubmitField()



class edit_package_form(FlaskForm):
    name = StringField("Name: ", validators=[validators.Length(min=3, max=200),DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5), DataRequired()])
    price = BetterDecimalField("Actual Price: ", validators=[DataRequired(message='You need to input a number!')])
    expiry_duration = IntegerField("Valid for (days):", validators=[DataRequired(message='You need to input a number!')])
    sessions = IntegerField("Number of Sessions:", validators=[validators.NumberRange(min=1), DataRequired(message='You need to input a number!')])
    discount = IntegerField("Discount(%): ", validators=[validators.NumberRange(min=0, max=100), validators.input_required()])
    image = FileField("Image of product: ", validators=[FileAllowed(images, 'Image only!')])
    submit = SubmitField()



class edit_service_form(FlaskForm):
    name = StringField("Name: ", validators=[validators.Length(min=3, max=200),DataRequired()])
    description = TextAreaField("Description: ", validators=[validators.Length(min=5, max=2000), DataRequired()])
    price = BetterDecimalField("Actual Price: ", validators=[validators.NumberRange(min=1),DataRequired(message='You need to input a number!')])
    image = FileField("Image of product: ", validators=[FileAllowed(images ,'Image only!')])
    discount = IntegerField("Discount(%): ", validators=[validators.NumberRange(min=0, max=100), validators.input_required()])
    submit = SubmitField()

class edit_coupon_form(FlaskForm):
    couponcode = StringField("Coupon Code: ", validators=[validators.Length(min=5, max=10),DataRequired()])
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



class checkout_form(FlaskForm):
    full_name = StringField("Full Name *: ", validators=[validators.Length(min=3, max=200), DataRequired()])
    country = SelectField('Country *:', validators=[DataRequired()], choices=[('Singapore', 'Singapore'), ('Malaysia', 'Malaysia'), ('Thailand', 'Thailand')])
    street_addr = StringField("Street Address *: ", validators=[validators.Length(min=3, max=200), DataRequired()])
    city = StringField("Town / City *: ", validators=[validators.Length(min=3, max=200), DataRequired()])
    postal = StringField("Postcode / ZIP *: ", validators=[validators.Length(min=3, max=200), DataRequired()])
    phone = StringField("Phone *: ", validators=[validators.Regexp(r'^(?:\+?65)?[689]\d{7}$', message= 'Phone number needs to start with 6,8 or 9'),validators.Length(min=3, max=200), DataRequired()])
    email = StringField("Email Address *: ", validators=[validators.Regexp(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$', message= 'Your email is invalid. Please check your email address.'),validators.Length(min=3, max=200), DataRequired()])
    card_name = StringField(" Name on Card *: ", validators=[validators.Length(min=3, max=200), DataRequired()])
    credit_card = StringField(" Credit card number *: ", validators=[validators.Regexp(r'^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$'),validators.Length(min=3, max=200), DataRequired()])
    exp_month = SelectField(" Expiry Month *: ", validators=[ DataRequired()], choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12')])
    exp_year = SelectField(" Expiry Year *: ", validators=[validators.Length(min=3, max=200), DataRequired()], choices=[('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026')])
    CVV = StringField(" CVV / CSV *: ", validators=[validators.Length(min=3, max=4), DataRequired()])
    submit = SubmitField()
