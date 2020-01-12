from flask_wtf import FlaskForm
from wtforms import *
import wtforms.validators as validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
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



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
