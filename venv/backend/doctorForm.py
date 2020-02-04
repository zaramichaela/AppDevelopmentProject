from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,DecimalField,TextAreaField,IntegerField,DateField, validators, PasswordField,SelectField
from flask_wtf.file import FileField, FileRequired,FileAllowed
from wtforms import Form, StringField, RadioField, SelectField,TextAreaField, validators
from flask_uploads import UploadSet, IMAGES,configure_uploads
images = UploadSet('images', IMAGES)

class CreatedoctorForm(FlaskForm):
    Name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    Specialities = SelectField('Specialities', [validators.DataRequired()], choices = [('', 'Select'), ('Gynaecology', 'Gynaecology'), ('Acupuncture', 'Acupuncture'),('General Wellness', 'General Wellness'),('Internal Medicine', 'Internal Medicine'),('Dermatology','Dermatology'), ('Paediatrics', 'Paediatrics')], default='')
    gender = SelectField('Gender', [validators.DataRequired()], choices = [('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    Profile = TextAreaField('Profile', [validators.Optional()])
    Status = SelectField('Status', [validators.DataRequired()], choices = [('', 'Select'), ('A', 'Available'), ('NA', 'Not Available')], default='')
    Image = FileField("Image of Doctor: ", validators=[FileAllowed(images ,'Image only!'), FileRequired('File was empty!')])
    submit = SubmitField()

