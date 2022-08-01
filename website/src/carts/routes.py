# Flask utilities
from flask import Blueprint, flash, redirect, render_template, request, url_for, flash, session
from flask_login import login_required, current_user
# Product model and routes
from ..products.models import AddProduct, Brand, Category
from ..products.routes import brands_query, categories_query
# JSON
import json
# Faker
# Every time a purchase is made a random date is given to it (between 2020-2022);
# This is for test purposes (so I have date variety in the dashboards);
# It can easily be undone and the 'real' date be given instead.
from faker import Faker


faker = Faker()
carts = Blueprint('carts', __name__)

def merge_dict(d1, d2):
    '''If Customer makes a purchase of various different items, information about both has to be stored.
    This function will be used later to merge dictionaries, if necessary, as each individual product has 
    its own dictionary. So, a purchase of 5 different products: 5 dictionaries, merged together,
    with the product ids as keys.'''

    if isinstance(d1, list) and isinstance(d2, list):
        return d1 + d2
    elif isinstance(d1, dict) and isinstance(d2, dict):
        return dict(list(d1.items()) + list(d2.items()))
    return False

@carts.route('/add-cart', methods=['POST'])
@login_required
def add_to_cart():
    '''
    From the Store page the Customer can add products to a personal cart, which contains all the information about the purchase.
    '''
    try:
        # The name I am getting: 'product_id' is defined in the details.html page in the form -> name="product_id"
        # Same for 'quantity' and 'quality'
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        color = request.form.get('colors')

        product = AddProduct.query.filter_by(id=product_id).first()
        # Get the brand and category names of each product added to the cart
        brand = Brand.query.filter_by(id=product.brand_id).first()
        category = Category.query.filter_by(id=product.category_id).first()
        # Get the company that is selling the product        
        # Check if user selected everything about the product
        if product_id and quantity and color and request.method == 'POST':
            
            #print('PRODUCT BRAND', brand.brand_name)
            #print('PRODUCT CATEGORY', category.category_name)
            #print('PRODUCT COMPANY', product.company)

            # The goal here is to create a fake date for when the products are purchased from the Store.
            # The main intention is to test the dashboards with different purchase dates, in order to not have all
            # of the puchases made in a 1-2 days timespan. 
            purchase_date = json.dumps(faker.date_time_between(start_date='-2y', end_date='now'), indent=4, sort_keys=True, default=str)

            # Make a Dictionary to hold the purchase information
            purchase_dict = {
                product_id:{
                    'name': product.name,
                    'purchase_date': purchase_date,
                    'company': product.company,
                    'unit_price': product.unit_price,     
                    'unit_cost': product.unit_cost,                   
                    'unit_discount': product.unit_discount,
                    'origin_country': product.origin_country,
                    'color': color,
                    'colors': product.colors,
                    'quantity': int(quantity),
                    'image': product.image,
                    'brand': brand.brand_name,
                    'category': category.category_name,
                    'customer_age': current_user.age
                    }}
            
            # print('DICT', purchase_dict)
            
            if 'ShoppingCart' in session:
                # If user adds to cart the same item multiple items from the store page increment 1 on the quantity value of the session dictionary
                if product_id in session['ShoppingCart']:
                    for key, value in session['ShoppingCart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            value['quantity'] += 1
                else:
                    session['ShoppingCart'] = merge_dict(session['ShoppingCart'], purchase_dict)
            else:
                session['ShoppingCart'] = purchase_dict
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@carts.route('/personal-cart', methods=['POST', 'GET'])
@login_required
def personal_cart():
    '''The last route the Customer sees before confirming the purchase.'''

    # If no purchases have been made, return to store
    if 'ShoppingCart' not in session or len(session['ShoppingCart']) <= 0:
        return redirect(url_for('products.store'))
    # Else make some basic calculations about pay total to display on the Customer Cart
    temp_total = 0
    pay_total = 0
    discount = 0
    for key, product in session['ShoppingCart'].items():
        # apply discount per item
        discount = (product['unit_discount']/100) * float(product['unit_price'])
        # Get total cost without discount 
        temp_total += float(product['unit_price']) * int(product['quantity'])
        # Apply discount
        temp_total -= discount
        # Apply Tax of 6%
        tax = float('%.2f' % ((1.06 * float(temp_total) - temp_total)))
        # Get total pay for all products with discount applied 
        pay_total = float('%.2f' % (temp_total + tax))
    return render_template('products/personal-cart.html',
    tax=tax,
    pay_total=pay_total,
    brands=brands_query(),
    categories=categories_query())

@carts.route('/update-cart/<int:id>', methods=['POST'])
@login_required
def update_cart(id):
    '''The customer has the hability to update 2 aspects of its order: each item's color and quantity.'''

    # If there is no cart yet, or no cart items, send user to the store
    if 'ShoppingCart' not in session or len(session['ShoppingCart']) <= 0:
        return redirect(url_for('products.store'))
    if request.method == 'POST':
        # Get the names for quantity and color present in the form
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try: 
            # Send the updated session cookie to the client
            session.modified = True
            for key, value in session['ShoppingCart'].items():
                # Get the product I want to delete by checking the id
                if int(key) == id:
                    value['color'] = color
                    value['quantity'] = quantity
                    flash('Item updated!', 'success')
                    return redirect(url_for('carts.personal_cart'))
        except Exception as e:
            print(e)
            return redirect(url_for('carts.personal_cart'))

@carts.route('/delete-cart-item/<int:id>', methods=['GET'])
@login_required
def delete_cart_item(id):
    # If there is no cart yet, or no cart items, send user to the store
    if 'ShoppingCart' not in session or len(session['ShoppingCart']) <= 0:
        return redirect(url_for('products.store'))
    try:        
        session.modified = True
        for key, value in session['ShoppingCart'].items():
            if int(key) == id:
                session['ShoppingCart'].pop(key, None)
                flash('Item removed!', 'warning')
                return redirect(url_for('carts.personal_cart'))

    except Exception as e:
        print(e)
        return redirect(url_for('carts.personal_cart'))

@carts.route('/empty')
@login_required
def empty_cart():
    try:
        session.pop('ShoppingCart', None)
        return redirect(url_for('products.store'))
    except Exception as e:
        print(e)
