from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators

class CreateUserForm(Form):
    firstName = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    membership = RadioField('Membership', choices=[('S', 'Silver'), ('G', 'Gold'), ('P', 'Platinum')], default='F')
    gender = SelectField('Color', [validators.DataRequired()], choices=[('', 'Select'), ('B', 'Black'), ('W', 'White')], default='')
    remarks = TextAreaField('Remarks', [validators.Optional()])

