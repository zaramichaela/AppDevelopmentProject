from wtforms import Form, StringField, RadioField, SelectField,TextAreaField, validators

class CreateUserForm(Form):
 ProductID = StringField('Product ID', [validators.Length(min=1,max=150), validators.DataRequired()])
 ProductName = StringField('Product Name', [validators.Length(min=1,max=150), validators.DataRequired()])
 Cost = StringField('Cost', [validators.Length(min=1,max=150),validators.DataRequired()])
 UserID = StringField('UserID'[validators.Length(min=1,max=150),validators.DataRequired()])

