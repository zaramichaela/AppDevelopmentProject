# from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, PasswordField, validators
from wtforms.validators import DataRequired

class customer_login_form(Form):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField()


