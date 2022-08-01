# Flask utilities
from flask import Blueprint, flash, redirect, render_template, request, url_for, flash, session, current_app
from flask_login import login_required, login_user, logout_user, current_user
# Werkzeug utilities
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
# Profile picture stuff
import uuid as uuid
# OS
import os
# Supplier model and form
from .forms import SupplierCompanyForm, SupplierLoginForm
from .models import Supplier
# Product model and form
from ..products.models import AddProduct, Brand, Category
from ..products.forms import AddProductForm
# Import db 
from ..extensions import db
# Import function to save image to database as string
from ..admin.routes import save_image
# Create CSV files for the dashboard
from ..plotlydash.create_csv import create_all_csv
# Password requirements when registering
from ..config import check_pass_strength

s_route = Blueprint('s_route', __name__)

#=========================================================================================== Supplier Register
@s_route.route('/register', methods=['GET', 'POST'])
def supplier_register():

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'supplier':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    form = SupplierCompanyForm()
    if form.validate_on_submit():        
        
        if check_pass_strength(form.password.data):
            flash("Password not strong enough. Must be of length 8 contain and 1 capital and 1 number.", "danger")
            return redirect(url_for('s_route.supplier_register'))

        hashed_password = generate_password_hash(form.password.data, 'sha256')
        new_supplier = Supplier(
            name = form.name.data,
            address = form.address.data,
            zip_code = form.zip_code.data,
            email = form.email.data,
            phone_contact_1 = form.phone_contact_1.data,
            phone_contact_2 = form.phone_contact_2.data,
            password = hashed_password,
            # save_image imported from 
            logo = save_image(request.files.get('logo'))
        )
        # Check for alredy existing Email and Name
        email = request.form.get('email')
        name = request.form.get('username')
        check_email = Supplier.query.filter_by(email=email).first()
        check_name = Supplier.query.filter_by(name=name).first()

        if check_email:
            flash("Please use a different email.", 'warning')
            return redirect(url_for('s_route.supplier_register'))
        if check_name:
            flash("Please use a different username.", 'warning')
            return redirect(url_for('s_route.supplier_register'))

        db.session.add(new_supplier)
        db.session.commit()
        flash(f'{form.name.data} registration successfull!', 'success')
        return redirect(url_for('s_route.supplier_login'))

    return render_template('supplier/register.html', form=form)

#=========================================================================================== Supplier Login
@s_route.route('/login', methods=['GET', 'POST'])
def supplier_login():
    '''
    Login as a Supplier with an email. The function will query for
    the first and ONLY email equal to the one being used to login. If it does not
    find it, a message is flashed. Same process for the password.
    If a Supplier logs in successfully, it is redirected to its profile page.
    
    When trying to log in with dummy users, a condition can be passed when checking
    the password:

    => if check_password_hash(user.password, form.password.data) or form.password.data == '123':

    Every dummy user created has a the same password, '123', and in order to log in as one
    this condition has to be created bellow.
    '''

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'supplier':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    form = SupplierLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        supplier = Supplier.query.filter_by(email=form.email.data).first_or_404()
        # Check is user exists
        if supplier:
            # Check if password is correct
            if check_password_hash(supplier.password, form.password.data) or form.password.data == '123':
                session['email'] = form.email.data
                session['permission'] = supplier.permission
                login_user(supplier, remember=True)
                flash(f'Welcome {form.email.data}! You are loged in!', 'success')
                return redirect(url_for('s_route.profile'))
            else:
                flash('Wrong Password!', 'danger')
        else:
            flash('Wrong Email!', 'danger')

    return render_template('supplier/login.html', form=form, supplier=current_user)

#=========================================================================================== Supplier Logout
@s_route.route('/logout')
@login_required
def supplier_logout():

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'supplier':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    logout_user()
    session.clear()
    return redirect(url_for('products.store'))

#=========================================================================================== Supplier Profile
@s_route.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'supplier':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))
    
    form = SupplierCompanyForm()
    supplier_id = current_user.id
    update_pro = Supplier.query.get_or_404(supplier_id)  
    if request.method == 'POST':
        update_pro.name = request.form['name']
        update_pro.address = request.form['address']
        update_pro.email = request.form['email']
        update_pro.zip_code = request.form['zip_code']
        update_pro.phone_contact_1 = request.form['phone_contact_1']
        update_pro.phone_contact_2 = request.form['phone_contact_2']
        # Check for Logo
        if request.files['logo']:
            update_pro.logo = request.files['logo']
            # Grab Image Name
            pic_filename = secure_filename(update_pro.profile_pic.filename)
			# Set UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
			# Save That Image
            saver = request.files['logo']

            # Change it to a string to save to db
            update_pro.profile_pic = pic_name
            try:
                db.session.commit()
                saver.save(os.path.join('static', pic_name))
                flash("User Updated Successfully!", 'success')
                return render_template("supplier/profile.html", 
					form=form,
					update_pro = update_pro)
            except:
                flash("Error!  Looks like there was a problem...try again!", 'warning')
                return render_template("supplier/profile.html", 
					form=form,
					update_pro = update_pro)
        else:
            return render_template('supplier/profile.html',
            form=form, 
            update_pro=update_pro)
    else:
        return render_template("supplier/profile.html", 
				form=form,
				update_pro = update_pro,
				supplier_id = supplier_id) 
 
#=========================================================================================== Supplier Update Profile
@s_route.route('/update-profile/<int:id>', methods=['GET', 'POST'])
@login_required
def update_profile(id):

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'supplier':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    supplier = Supplier.query.get_or_404(id)
    form = SupplierCompanyForm(request.form) 
    # If the user actually updates the supplier, the database must be updated:
    if request.method == 'POST':
        supplier.name = form.name.data
        supplier.address = form.address.data
        supplier.zip_code = form.zip_code.data
        supplier.email = form.email.data
        supplier.phone_contact_1 = form.phone_contact_1.data
        supplier.phone_contact_2 = form.phone_contact_2.data
        # Check for image update
        if request.files.get('logo'):
            # The following import had to be done here due to circular imports
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/' + supplier.logo))
                supplier.logo = save_image(request.files.get('logo'))
            except:
                supplier.logo = save_image(request.files.get('logo'))

        db.session.commit()
        flash(f'{form.name.data} has been updated!', 'success')
        return redirect(url_for('s_route.supplier_view_edit'))
        
    # Fill the fields with the values alredy in the database
    form.name.data = supplier.name
    form.address.data = supplier.address
    form.zip_code.data = supplier.zip_code
    form.email.data = supplier.email 
    form.phone_contact_1.data = supplier.phone_contact_1                                                                        
    form.phone_contact_2.data = supplier.phone_contact_2
    return render_template('supplier/update.html',
    form=form,
    supplier=supplier)

#=========================================================================================== DashBoard
@s_route.route("/dash-supplier", methods=["GET"])
@login_required
def supplier_dashboard():  
    '''
    Show the current logged in Supplier Dashboard
    '''  

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'supplier':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    #print('CURRENT USER NAME', current_user.name)    
    if current_user.is_authenticated:
        create_all_csv()
        session['username'] = current_user.name
    return render_template('supplier/dash.html')

#=========================================================================================== New Product
@s_route.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():  

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'supplier':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))

    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProductForm(request.form)
    suppliers = Supplier.query.filter_by(id=current_user.id).first_or_404()
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

        new_product.company = suppliers.name
        db.session.add(new_product)
        db.session.commit()
        flash('Product created!', 'success')
        return redirect(url_for('s_route.supplier_view_edit'))
    return render_template('products/add-product.html',
    form=form,
    brands=brands,
    categories=categories,
    session=session)

#=========================================================================================== Update Product
@s_route.route('/update-product/<int:id>', methods=['GET', 'POST'])
@login_required
def update_product(id):

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'supplier':
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
            # The following import had to be done here due to circular imports
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/' + product.image))
                product.image = save_image(request.files.get('image'))
            except:
                product.image = save_image(request.files.get('image'))

        db.session.commit()
        flash(f'{form.name.data} has been updated!', 'success')
        return redirect(url_for('s_route.supplier_view_edit'))
        
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
@s_route.route('/delete-product/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_product(id):

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'supplier':
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
        
        flash(f'{product.name} has been deleted!', 'success')        
        return redirect(url_for('s_route.supplier_view_edit'))

    flash('Cant delete the selected product.', 'danger')    
    return redirect(url_for('s_route.supplier_view_edit'))
#=========================================================================================== Supplier View & Edit
@s_route.route('/view-edit')
@login_required
def supplier_view_edit():

    # Make sure customers cant access this page
    if 'permission' in session:
        if session['permission'] != 'supplier':
            flash('You are not allowed to visit this page!', 'warning')
            return redirect(url_for('products.store'))
            
    if 'email' not in session:
        flash('Please login first!', 'danger')
        if session['permission'] == 'supplier':
            return redirect(url_for('s_route.supplier_login'))
        elif session['permission'] == 'admin':
            return redirect(url_for('admin_route.login'))
    products = AddProduct.query.filter_by(company=current_user.name)
    return render_template('supplier/view_edit.html', products=products)

