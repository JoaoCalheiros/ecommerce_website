# Flask utilities
from flask import Blueprint, flash, redirect, render_template, request, url_for, flash, session, make_response
from flask_login import login_required, login_user, logout_user, current_user
# Werkzeug utilities
from werkzeug.security import generate_password_hash, check_password_hash
# Customer model and form
from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Register, CustomerOrder
# Product model
from ..products.models import AddProduct
# Import db 
from ..extensions import db
# Personal order code
import secrets
# Generate PDF 
import pdfkit
# Password requirements when registering
from ..config import check_pass_strength

customer_route = Blueprint('customer_route', __name__)

@customer_route.route('/')
def home():
    return redirect(url_for('products.store'))

#=========================================================================================== Customer Register
@customer_route.route('/register', methods=['GET', 'POST'])
def customer_register():

    '''Register a new Customer. Customers only have access to the Store page,
    the Details page of each product and their personal Cart.
    This function will register a new user, checking for alredy existing
    chosen username and email, while storing the new user information on
    the Database.'''

    form = CustomerRegisterForm()
    if form.validate_on_submit():
        
        if check_pass_strength(form.password.data):
            flash("Password not strong enough. Must be of length 8 contain and 1 capital and 1 number.", "danger")
            return redirect(url_for('customer_route.customer_register'))

        hashed_password = generate_password_hash(form.password.data, 'sha256')
        new_user = Register(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            username = form.username.data,
            age = form.age.data,
            email = form.email.data,
            country = form.country.data,
            city = form.city.data,
            district = form.district.data,
            current_address = form.current_address.data,
            zip_code = form.zip_code.data,
            phone_contact = form.phone_contact.data,
            password = hashed_password)

        # Check for alredy existing Email, Username and Phone Contact
        email = request.form.get('email')
        username = request.form.get('username')
        phone_contact = request.form.get('phone_contact')
        check_email = Register.query.filter_by(email=email).first()
        check_username = Register.query.filter_by(username=username).first()
        check_phone = Register.query.filter_by(phone_contact=phone_contact).first()

        if check_email:
            flash("Email alredy in use!", "danger")
            return redirect(url_for('customer_route.customer_register'))
        elif check_username:
            flash("Username alredy in use!", "danger")
            return redirect(url_for('customer_route.customer_register'))
        elif check_phone:
            flash("Phone contact alredy in use!", "danger")
            return redirect(url_for('customer_route.customer_register'))
        
        db.session.add(new_user)
        db.session.commit()
        flash(f"{username} registration successfull!")
        return redirect(url_for('customer_route.customer_login'))

    return render_template('customer/register.html', form=form)

#=========================================================================================== Customer Login
@customer_route.route('/login', methods=['GET', 'POST'])
def customer_login():

    '''Login as a Customer with an email. The function will query for
    the first and ONLY email equal to the one being used to login. If it does not
    find it, a message is flashed. Same process for the password.
    If a Customer logs in successfully, it is redirected to the Store page.
    
    When trying to log in with dummy users, a condition can be passed when checking
    the password:

    => if check_password_hash(user.password, form.password.data) or form.password.data == '123':

    Every dummy user created has a the same password, '123', and in order to log in as one
    this condition has to be created bellow.
    '''

    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        # Check if email exists
        if user:
            # Check password 
            if check_password_hash(user.password, form.password.data):
                session['permission'] = user.permission
                login_user(user)
                flash('Loged in!', 'success')
                next_page_requested = request.args.get('next')
                return redirect(next_page_requested or url_for('products.store'))
            else:
                flash('Wrong Password!', 'danger')
                return redirect(url_for('customer_route.customer_login'))
        else:
            flash('Email does not exist!', 'danger')
            return redirect(url_for('customer_route.customer_login'))
    return render_template('customer/login.html', form=form)

#=========================================================================================== Customer Logout
@customer_route.route('/logout')
@login_required
def customer_logout():
    logout_user()
    session.clear()
    return redirect(url_for('products.store'))

#=========================================================================================== Customer Purchase Order
@customer_route.route('/getorder')
@login_required
def get_order():

    '''
    Register the Customer order. Save its details in the Database on the
    customer_order table on the orders column.
    Make changes to the inventory column on the all_products table, depending
    on how many products the Customer bought. When the Customer confirms its
    purchase it will be redirected to the order it just registered.
    '''

    # Double check
    customer_id = current_user.id
    if current_user.is_authenticated:
        customer_id = current_user.id
        code = secrets.token_hex(5)
        try:
            order = CustomerOrder(code=code, customer_id=customer_id, orders=session['ShoppingCart'])
            db.session.add(order)
            db.session.commit()

            # Makes changes to the DB on the inventory part
            for key, product in session['ShoppingCart'].items():
                quantity = int(product['quantity'])
                product_query = AddProduct.query.filter_by(id=key).all()
                # print('KEY:', key, 'QUANTITY:', quantity)
                product_inventory = [p.inventory for p in product_query]
                product_inventory = product_inventory[0] - int(quantity)
                # print('product_inventory', product_inventory)

                for i in product_query:
                    i.inventory = product_inventory
                    db.session.commit()

            flash('Your order has been sent!', 'success')
            session.pop('ShoppingCart')
            return redirect(url_for('customer_route.show_orders',code=code))
        except Exception as e:
            print(e)
            flash('Problems in get_order', 'danger')
            return redirect(url_for('carts.personal_cart'))

#=========================================================================================== Customer See Personal Purchase
@customer_route.route('/orders/<code>')
@login_required
def show_orders(code):

    '''
    When a Customer confirms the purchase this is the route they are redirected to.
    It shows them the full purchase details of what they just ordered, the tax implemented
    on their products as well as the delivery status and code.
    '''

    if current_user.is_authenticated:
        customer_id = current_user.id
        temp_total = 0
        pay_total = 0
        customer_query = Register.query.filter_by(id=customer_id).first()
        orders_query = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first() 

        for key, product in orders_query.orders.items():
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

    else:
        return redirect(url_for('customer_route.customer_login'))    
    return render_template('customer/order.html',
    code=code, 
    tax=tax,
    pay_total=pay_total,
    customer_query=customer_query,
    orders_query=orders_query)

#=========================================================================================== Customer PDF
@customer_route.route('/pdf/<code>', methods=['POST'])
@login_required
def get_pdf(code):

    if current_user.is_authenticated:
        customer_id = current_user.id
        temp_total = 0
        pay_total = 0
        if request.method == 'POST':

            customer_query = Register.query.filter_by(id=customer_id).first()
            orders_query = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first() 

            for key, product in orders_query.orders.items():
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

            rendered = render_template('customer/pdf.html',
            code=code, 
            tax=tax,
            pay_total=pay_total,
            customer_query=customer_query,
            orders_query=orders_query)

            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            # To instantly download the pdf use 'attachment' instead of 'inline'
            response.headers['Content-Disposition'] = 'inline; filename=' + code + '.pdf'
            return response
    return redirect(url_for('customer_route.show_orders'))
