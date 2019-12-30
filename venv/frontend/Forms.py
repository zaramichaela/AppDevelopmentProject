from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators


class CreateUserForm(Form):
    firstName = StringField('FirstName', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('LastName', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    date_of_birth = SelectField('Day', [validators.length(min=1, max=31), validators.DataRequired()], 'Month', [validators.length(min=1, max=12), validators.DataRequired()],
                                'Year', [validators.length(''), validators.DataRequired()])

