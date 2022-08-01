# FLask utilities
from flask_login import UserMixin
# Datetime
from datetime import datetime
# Import db
from ..extensions import db

class Supplier(db.Model, UserMixin):
    __tablename__ = 'suppliers_table' 

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=False)
    address = db.Column(db.String(50), unique=False)
    zip_code = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    phone_contact_1 = db.Column(db.String(50), unique=False)
    phone_contact_2 = db.Column(db.String(50), unique=False)
    password = db.Column(db.String(50), unique=False)
    logo = db.Column(db.String(200), default='profile.jpg')
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    permission = db.Column(db.String(10), nullable=False, default='supplier')
