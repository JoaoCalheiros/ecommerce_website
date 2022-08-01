# Flask utilities
from flask_wtf.file import FileAllowed, FileField
from flask_wtf import FlaskForm
# WTForms utilities
from wtforms import StringField, PasswordField, IntegerField, SubmitField, validators


class SupplierCompanyForm(FlaskForm):
    name = StringField('Company Name', [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])
    zip_code = StringField('Zip Code', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    phone_contact_1 = IntegerField('Phone Contact', [validators.DataRequired()])
    phone_contact_2 = IntegerField('Phone Contact (secondary)', [validators.DataRequired()])        
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('password_check', message='Passwords must match!')])
    password_check = PasswordField('Confirm Password', [validators.DataRequired()])
    logo = FileField('Company Logo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Image only please')])
    submit = SubmitField('Finalize Registration')

class SupplierLoginForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])

