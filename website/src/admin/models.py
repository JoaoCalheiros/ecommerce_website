# Flask utilities
from flask_login import UserMixin
# Import db
from ..extensions import db


class AdminUser(db.Model, UserMixin):
    __tablename__ = 'admin_table'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100))
    first_name = db.Column(db.String(50), nullable=False) 
    last_name = db.Column(db.String(50), nullable=False) 
    age = db.Column(db.String(50), nullable=False) 
    country = db.Column(db.String(50), nullable=False)
    permission = db.Column(db.String(10), nullable=False, default='admin')    

