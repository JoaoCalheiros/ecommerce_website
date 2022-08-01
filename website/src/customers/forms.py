# Flask utilities
from flask_wtf.file import FileAllowed, FileField
from flask_wtf import FlaskForm
# WTForms utilities 
from wtforms import StringField, PasswordField, IntegerField, SubmitField, validators

class CustomerRegisterForm(FlaskForm):
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    username = StringField('Username', [validators.DataRequired()])
    age = StringField('Age', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])    
    country = StringField('Country', [validators.DataRequired()])
    city = StringField('City', [validators.DataRequired()])
    district = StringField('District', [validators.DataRequired()])
    current_address = StringField('Current Address', [validators.DataRequired()])
    zip_code = StringField('Zip Code', [validators.DataRequired()])    
    phone_contact = IntegerField('Phone Contact', [validators.DataRequired()])    
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('password_check', message='Passwords must match!')])
    password_check = PasswordField('Confirm Password', [validators.DataRequired()])
    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Image only please')])
    submit = SubmitField('Finalize Registration')

class CustomerLoginForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
