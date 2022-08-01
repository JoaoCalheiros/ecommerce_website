# Flask utilities
from flask_login import UserMixin
# Datetime
from datetime import datetime
# JSON
import json
# Import db
from ..extensions import db


class Register(db.Model, UserMixin):
    __tablename__ = 'customers_table' 
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(50), unique=False)
    last_name = db.Column(db.String(50), unique=False)
    username = db.Column(db.String(50), unique=True)
    age = db.Column(db.Integer())
    email = db.Column(db.String(50), unique=True)
    country = db.Column(db.String(50), unique=False)
    city = db.Column(db.String(50), unique=False)
    district = db.Column(db.String(50), unique=False)
    current_address = db.Column(db.String(50), unique=False)
    zip_code = db.Column(db.String(50), unique=False)
    phone_contact = db.Column(db.String(50), unique=False)
    password = db.Column(db.String(50), unique=False)
    profile_pic = db.Column(db.String(200), default='profile.jpg')
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow) 
    permission = db.Column(db.String(10), nullable=False, default='customer')

class JsonEncondeDict(db.TypeDecorator):     
    '''Method to dump personal cart information (dictionary) into the orders table column as valid JSON'''

    impl = db.Text   
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerOrder(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(50), unique=False)
    status = db.Column(db.String(50), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer(), unique=False, nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    orders = db.Column(JsonEncondeDict)



