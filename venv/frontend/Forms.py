from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators

class UserForm(Form):
    firstName = StringField('FirstName', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('LastName', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices = [('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
