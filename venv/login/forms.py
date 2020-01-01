from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,DecimalField,TextAreaField,IntegerField,DateField, PasswordField
from flask_wtf.file import FileField, FileRequired,FileAllowed
from wtforms.validators import DataRequired
import wtforms.validators as validators
import os
import re

class admin_login_form(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])

class create_admin_login(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    cfm_password = PasswordField("Confirm Password:", validators=[DataRequired()])
