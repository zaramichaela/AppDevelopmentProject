from flask_wtf import FlaskForm
from wtforms import *
import wtforms.validators as validators
from wtforms.validators import DataRequired
from login.user_account import *

class admin_login_form(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField()

class create_admin_account(FlaskForm):
    username = StringField("Username:", validators=[validators.Length(min=3, max=12) ,DataRequired()])
    password = PasswordField("Password:", validators=[validators.Length(min=8, max=16) ,DataRequired(), validators.EqualTo('cfm_password', message='Passwords must match')])
    cfm_password = PasswordField("Confirm Password:", validators=[validators.Length(min=8, max=16) ,DataRequired()])
    submit = SubmitField()

class customer_registration(FlaskForm):
    username = StringField("Username:", validators=[validators.Length(min=3, max=20), DataRequired()])
    email = StringField("Email:", validators=[validators.Length(min=6, max=60), DataRequired()])
    password = PasswordField("Password:", validators=[validators.Length(min=8, max=20), DataRequired(), validators.EqualTo('cfm_password', message='Password must match')])
    cfm_password = PasswordField("Confirm Password:", validators=[validators.Length(min=8, max=20), DataRequired()])
    submit = SubmitField()



class UserLogin(Form):
    username = StringField("Username:", validators=[validators.Length(min=3, max=20), DataRequired()])
    password = PasswordField("Password:", validators=[validators.Length(min=8, max=20), DataRequired()])
    submit = SubmitField()


class create_admin(Form):
    username = StringField("Username:", validators=[validators.Length(min=3, max=12), DataRequired()])
    password = PasswordField("Password:", validators=[validators.Length(min=4, max=18), DataRequired(), validators.EqualTo('cfm_password', message='Password must match')])
    cfm_password = PasswordField("Confirm Password:", validators=[validators.Length(min=4, max=18), DataRequired()])
    submit = SubmitField()


class AdminLogin(Form):
    username = StringField("Username:", validators=[validators.Length(min=3, max=12), DataRequired()])
    password = PasswordField("Password:", validators=[validators.Length(min=4, max=18), DataRequired()])
    submit = SubmitField()
