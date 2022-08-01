# Flask utilities
from flask import Blueprint, flash, redirect, render_template, request, url_for, flash, session, current_app
from flask_login import login_user, login_required, logout_user, current_user
# Werkzeug utilities
from werkzeug.security import generate_password_hash, check_password_hash
# Admin model and form
from .forms import LoginForm, RegisterForm
from .models import AdminUser
# Product model and form
from ..products.forms import AddProductForm
from ..products.models import AddProduct, Brand, Category
# Supplier model
from ..supplier.models import Supplier
# Save image as string in database - related stuff
import os
import secrets
# Import db 
from ..extensions import db
# Password requirements when registering
from ..config import check_pass_strength

admin_route = Blueprint('admin_route', __name__)

def save_image(img):
    '''
    Function to save the selected image as a hashed string in
    the Database and in the static file.
    '''

    hash_img = secrets.token_urlsafe(10)
    print('IMG', img)
    _,file_extension = os.path.splitext(img.filename)
    img_name = hash_img + file_extension
    print('img name', img_name)
    file_path = os.path.join(current_app.root_path, 'static', img_name)
    print('PATH',file_path)
    img.save(file_path)
    return img_name

#=========================================================================================== Admin Register
@admin_route.route('/register', methods=['GET', 'POST'])
def register():

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        if check_pass_strength(form.password_hash.data):
            flash("Password not strong enough. Must be of length 8 contain and 1 capital and 1 number.", "danger")
            return redirect(url_for('admin_route.register'))

        # Hash the user password 
        hashed_password = generate_password_hash(form.password_hash.data, 'sha256')
        # Create a new user object
        admin_user = AdminUser(
            email=form.email.data,
            username=form.username.data,
            password_hash = hashed_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            age=form.age.data, 
            country=form.country.data)        
        db.session.add(admin_user)
        db.session.commit()
        flash(f'{form.first_name.data} registration is complete!', 'success')
        # If successfull, go to Login page
        return redirect(url_for('admin_route.login'))
    # If unsuccessfull remain in Register page
    return render_template('admin/register.html', form=form)

#=========================================================================================== Admin Login
@admin_route.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login as an Admin with an email. The function will query for
    the first and ONLY email equal to the one being used to login. If it does not
    find it, a message is flashed. Same process for the password.
    If a Admin logs in successfully, it is redirected to its view & edit page.
    
    When trying to log in with dummy users, a condition can be passed when checking
    the password:

    => if check_password_hash(user.password, form.password.data) or form.password.data == '123':

    Every dummy user created has a the same password, '123', and in order to log in as one
    this condition has to be created bellow.
    '''

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = AdminUser.query.filter_by(email=form.email.data).first()
        # Check is user exists
        if user:
            # Check if password is correct
            if check_password_hash(user.password_hash, form.password.data):
                # Get these 3 session variables as they will be used in various stages of the app
                session['email'] = form.email.data
                session['permission'] = user.permission
                session['username'] = user.username
                login_user(user, remember=True)
                flash(f'Welcome {form.email.data}! You are loged in!', 'success')
                return redirect(url_for('admin_route.admin_view_edit'))
            else:
                flash('Wrong password!', 'danger')
        else:
            flash('User does not exist!', 'danger')
    return render_template('admin/login.html',
    form=form,
    user=current_user)

#=========================================================================================== Admin Logout
@admin_route.route('/logout')
@login_required
def admin_logout():

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    logout_user()
    session.clear()
    return redirect(url_for('admin_route.login'))

#=========================================================================================== Admin Plots
@admin_route.route("/dash", methods=["GET"])
@login_required
def admin_dashboard():  

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store')) 

    return render_template('admin/dash.html')

#=========================================================================================== Brands
@admin_route.route('/brands')
@login_required
def brands():
    '''
    This route lets the Admin see every Brand created, edit and/or delete them.
    '''
    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_route.login'))
    brands = Brand.query.order_by(Brand.id.asc()).all()
    return render_template('admin/brand.html',
    brands=brands)

@admin_route.route('/add-brand', methods=['GET', 'POST'])
@login_required
def add_brand():
    '''
    This route is for Admins only. Only Admins can create/edit/delete
    new Brands and/or Categories.
    '''

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    if request.method == 'POST':
        get_brand = request.form.get('brand')
        brand = Brand(brand_name=get_brand)
        flash(f'{get_brand} was added to the database.', 'success')
        db.session.add(brand)
        db.session.commit()
        return redirect(url_for('admin_route.admin_view_edit'))
    brands = Brand.query.order_by(Brand.id.asc()).all()
    return render_template('admin/add-brand.html',
    brands=brands)

@admin_route.route('/update-brand/<int:id>', methods=['GET', 'POST'])
@login_required
def update_brand(id):

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_route.login'))
    update_brand = Brand.query.get_or_404(id)
    # Get the name of the input field - the brand I wanna edit
    brand = request.form.get('brand')
    if request.method == 'POST':
        update_brand.brand_name = brand
        flash('Brand successfully updated', 'success')
        db.session.commit()
        return redirect(url_for('admin_route.brands'))
    return render_template('admin/update-brand-category.html',
    update_brand=update_brand)

@admin_route.route('/delete-brand/<int:id>', methods=['POST'])
@login_required
def delete_brand(id):
    brand = Brand.query.get_or_404(id)

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'{brand.brand_name} has been deleted!', 'success')
        return redirect(url_for('admin_route.admin_view_edit'))
    flash(f'{brand.brand_name} can\'t be deleted!', 'warning')
    return redirect(url_for('admin_route.brands'))

#=========================================================================================== Categories
@admin_route.route('/category')
@login_required
def categories():
    '''
    This route lets the Admin see every Category created, edit and/or delete them.
    '''

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_route.login'))
    categories = Category.query.order_by(Category.id.asc()).all()
    return render_template('admin/brand.html',
    categories=categories)
    
@admin_route.route('/add-category', methods=['GET', 'POST'])
@login_required
def add_category():
    '''
    This route is for Admins only. Only Admins can create/edit/delete
    new Brands and/or Categories.
    '''
    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    if request.method == 'POST':
        get_cat = request.form.get('category')
        category = Category(category_name=get_cat)
        flash(f'{get_cat} was added to your database.', 'success')
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('admin_route.admin_view_edit'))
    categories = Category.query.order_by(Category.id.asc()).all()
    return render_template('admin/add-brand.html',
    categories=categories)

@admin_route.route('/update-category/<int:id>', methods=['GET', 'POST'])
@login_required
def update_category(id):

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_route.login'))
    update_category = Category.query.get_or_404(id)
    # Get the name of the input field - the category I wanna edit
    category = request.form.get('category')
    if request.method == 'POST':
        update_category.category_name = category
        flash('Category successfully updated', 'success')
        db.session.commit()
        return redirect(url_for('admin_route.categories'))
    return render_template('admin/update-brand-category.html',
    update_category=update_category)

@admin_route.route('/delete-category/<int:id>', methods=['POST'])
@login_required
def delete_category(id):

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'{category.category_name} has been deleted!', 'success')
        return redirect(url_for('admin_route.admin_view_edit'))
    flash(f'{category.category_name} can\'t be deleted!', 'warning')
    return redirect(url_for('admin_route.categories'))

#=========================================================================================== New Product
@admin_route.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    '''
    An Admin can create a product, just like any Supplier. A default value of 'admin' 
    will be added to the all_products column 'company'.
    '''

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))
    
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProductForm(request.form)

    if request.method == 'POST':
        name = form.name.data
        description = form.description.data
        unit_price = form.unit_price.data
        unit_cost = form.unit_cost.data
        unit_discount = form.unit_discount.data
        inventory = form.inventory.data
        origin_country = form.origin_country.data
        colors = form.colors.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image = save_image(request.files.get('image'))

        new_product = AddProduct(name=name,
                                description=description,
                                unit_price=unit_price,
                                unit_cost=unit_cost,
                                unit_discount=unit_discount,
                                inventory=inventory,
                                origin_country=origin_country,
                                colors=colors,
                                brand_id=brand,
                                category_id=category,
                                image=image)

        # Give a default value of 'admin' to the company column every time an Admin creates a product.                
        new_product.company = 'admin' 
        db.session.add(new_product)
        db.session.commit()
        flash('Product created!', 'success')
        return redirect(url_for('admin_route.admin_view_edit'))

    return render_template('products/add-product.html',
    form=form,
    brands=brands,
    categories=categories,
    session=session)

#=========================================================================================== Update Product
@admin_route.route('/update-product/<int:id>', methods=['GET', 'POST'])
@login_required
def update_product(id):

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    brands = Brand.query.all()
    categories = Category.query.all()
    product = AddProduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')

    form = AddProductForm(request.form)       

    # If the user actually updates the product, the database must be updated:
    if request.method == 'POST':
        product.brand_id = brand
        product.category_id = category
        product.name = form.name.data
        product.description = form.description.data
        product.unit_price = form.unit_price.data
        product.unit_cost = form.unit_cost.data
        product.unit_discount = form.unit_discount.data
        product.inventory = form.inventory.data
        product.origin_country = form.origin_country.data
        product.colors = form.colors.data
        # Check for image update
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/' + product.image))
                product.image = save_image(request.files.get('image'))
            except:
                product.image = save_image(request.files.get('image'))

        db.session.commit()
        flash(f'{form.name.data} has been updated!', 'success')
        return redirect(url_for('admin_route.admin_view_edit'))        
        
    # Fill the fields with the values alredy in the database
    form.name.data = product.name
    form.description.data = product.description
    form.unit_price.data = product.unit_price
    form.unit_cost.data = product.unit_cost
    form.unit_discount.data = product.unit_discount
    form.inventory.data = product.inventory
    form.origin_country.data = product.origin_country                                                                        
    form.colors.data = product.colors
    return render_template('products/update-product.html',
    form=form,
    brands=brands,
    categories=categories,
    product=product,
    session=session)

#=========================================================================================== Delete Product
@admin_route.route('/delete-product/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_product(id):

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    product = AddProduct.query.get_or_404(id)
    if request.method == 'GET':
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/' + product.image))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        
        flash(f'{{product.name}} has been deleted!', 'success')
        return redirect(url_for('admin_route.admin_view_edit'))

    flash('Cant delete the selected product.', 'danger')
    return redirect(url_for('admin_route.admin_view_edit'))

#=========================================================================================== Admin View & Edit
@admin_route.route('/view-edit')
@login_required
def admin_view_edit():
    '''This is basically the Admin Home page. Here the admin can 
       see, edit and delete any the products from every supplier.
       The admin cannot, however, create a new product.'''

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    if 'email' not in session:
        flash('Please login first!', 'danger')
        # If current user is Admin return the Admin view and edit page
        if session['permission'] == 'admin':
            return redirect(url_for('admin_route.login'))
        else:
        # Else return the Supplier view and edit page
            return redirect(url_for('s_route.supplier_login'))
    
    products = AddProduct.query.all()
    return render_template('admin/view_edit.html',
    products=products)

#=========================================================================================== Admin View Suppliers List
@admin_route.route('/suppliers')
@login_required
def admin_view_suppliers():
    '''This route lets the Admin see a list with every current Supplier, 
    and their contacts. It is not possible for the Admin to delete any Supplier,
    as of right now.'''

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'admin':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    suppliers = Supplier.query.all()
    return render_template('admin/all_suppliers.html',
    suppliers=suppliers)
