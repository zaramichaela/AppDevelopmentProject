# from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, PasswordField, validators
from wtforms.validators import DataRequired

class customer_login_form(Form):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField()

class create_customer_account(Form):
    username = StringField("Username:", validators=[validators.Length(min=3, max=12), DataRequired()])
    email = StringField("Email:", validators=[validators.Length(min=6, max=16), DataRequired()])
    password = PasswordField("Password:", validators=[validators.Length(min=8, max=16), DataRequired(), validators.EqualTo('cfm_password', message='Password must match')])
    cfm_password = PasswordField("Confirm Password:", validators=[validators.Length(min=8, max=16), DataRequired()])
    submit = SubmitField()
