# Flask utilities
from flask_wtf.file import FileAllowed, FileField
# WTForms utilities 
from wtforms import Form, StringField, IntegerField, TextAreaField, FloatField
from wtforms.validators import DataRequired

class AddProductForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Product Description', validators=[DataRequired()])
    unit_price = FloatField('Unit Public Price', validators=[DataRequired()])
    unit_cost = FloatField('Unit Manufactoring Cost', validators=[DataRequired()])
    unit_discount = IntegerField('Unit Discount', default=0)
    inventory = IntegerField('Inventory', validators=[DataRequired()])
    origin_country = StringField('Origin Country', validators=[DataRequired()])
    delivery_company = StringField('Delivery Company', validators=[DataRequired()])
    colors = TextAreaField('Colors', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
