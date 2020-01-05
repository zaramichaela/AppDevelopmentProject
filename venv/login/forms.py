from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,DecimalField,TextAreaField,IntegerField,DateField, PasswordField,validators
from wtforms.validators import DataRequired
import wtforms.validators as validators
import os
import re

class admin_login_form(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField()

class create_admin_account(FlaskForm):
    username = StringField("Username:", validators=[validators.Length(min=3, max=12) ,DataRequired()])
    password = PasswordField("Password:", validators=[validators.Length(min=8, max=16) ,DataRequired(), validators.EqualTo('cfm_password', message='Passwords must match')])
    cfm_password = PasswordField("Confirm Password:", validators=[validators.Length(min=8, max=16) ,DataRequired()])
    submit = SubmitField()


