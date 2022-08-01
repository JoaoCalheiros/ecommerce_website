# Import db
from ..extensions import db

class AddProduct(db.Model):
    __tablename__ = 'products_table' 
    
    # Define columns to be able to search products
    __searchable__ = ['name', 'company', 'origin_country']   

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    unit_price = db.Column(db.Float(), nullable=False)
    unit_cost = db.Column(db.Float(), nullable=False)
    unit_discount = db.Column(db.Integer(), default=0)
    inventory = db.Column(db.Integer(), nullable=False)
    origin_country = db.Column(db.String(), nullable=False)
    colors = db.Column(db.Text(), nullable=False)   
    brand_id = db.Column(db.Integer(), db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))
    category_id = db.Column(db.Integer(), db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('categories', lazy=True))
    company = db.Column(db.String(), nullable=False, default='waiting for creation')
    image = db.Column(db.String(), nullable=True, default='default.jpg')


class Brand(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    brand_name = db.Column(db.String(100))

class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category_name = db.Column(db.String(100))

