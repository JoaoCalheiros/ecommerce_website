# Flask utilities
from flask import Blueprint, render_template, request, session
# Product models
from .models import Brand, Category, AddProduct

products = Blueprint('products', __name__)

#====================================================================================================================================================#
'''
The following 2 functions allows me to show, on the dropdown navbar link, ONLY the brands/categories which have an inventory value > 0.
If the inventory of a brand/category is <= 0 the brand/category wont be displayed in the dropdown menu.
'''

def brands_query():
    brands = Brand.query.join(AddProduct, (Brand.id == AddProduct.brand_id)).all()
    return brands

def categories_query():
    categories = Category.query.join(AddProduct, (Category.id == AddProduct.category_id)).all()
    return categories

    
#=========================================================================================== Store HomePage
@products.route('/store')
def store():
    '''
    The website 'Homepage'. Displays every product from every supplier.
    From here Customers can add products to their personal Cart, view 
    products Details, and search for products for Brand, Category or 
    product name, supplier (company) or origin country through the 
    search bar.
    '''

    # If there are multiple pages, always show the first one when entering the website
    page = request.args.get('page', 1, type=int)
    #print(session)

    # Filter products that we have in our inventory - order them by latests added to the site
    # per_page defines how many items will be displayed per page
    products = AddProduct.query.filter(AddProduct.inventory > 0).order_by(AddProduct.id.desc()).paginate(page=page, per_page=12)
    return render_template('products/store.html',
    products=products,
    brands=brands_query(),
    categories=categories_query(),
    session=session)

#=========================================================================================== Search Results
@products.route('/search-result')
def search_result():
    '''
    Search Bar
    '''
    search_word = request.args.get('search_word_input')
    # Table columns that the user can search for
    products = AddProduct.query.msearch(search_word, fields=['name', 'company', 'origin_country'], limit=50)
    return render_template('products/search-result.html',
    products=products,
    brands=brands_query(),
    categories=categories_query())

#=========================================================================================== Product Details Page
@products.route('/product/<int:id>')
def details_page(id):
    '''
    Each product's Details page. Grabd the product id and then some of
    its specificities in order to show them to the Customer.
    '''
    product = AddProduct.query.get_or_404(id)
    return render_template('products/details.html',
    product=product,
    brands=brands_query(),
    categories=categories_query())

#=========================================================================================== Filtered Products - By Brand
@products.route('/brand/<int:id>')
def show_selected_brand_products(id):    
    '''
    When customer selects a Brand, only show products from that Brand.
    '''

    # Define pages
    page = request.args.get('page', 1, type=int)
    # Get brand id
    product_brand_id = Brand.query.filter_by(id=id).first_or_404()
    # The brand_id is in the src.products.models.AddProduct Class
    product_brand = AddProduct.query.filter_by(brand=product_brand_id).paginate(page=page, per_page=10)
    return render_template('products/store.html',
    product_brand=product_brand,
    brands=brands_query(),
    categories=categories_query(),
    product_brand_id=product_brand_id)

#=========================================================================================== Filtered Products - By Category
@products.route('/category/<int:id>')
def show_selected_category_products(id):
    '''
    When customer selects a Category, only show products from that Category.
    '''

    # Define pages
    page = request.args.get('page', 1, type=int)
    # Get category id
    product_category_id = Category.query.filter_by(id=id).first_or_404()
    # The category=.. is in the src.products.models.AddProduct Class
    product_category = AddProduct.query.filter_by(category=product_category_id).paginate(page=page, per_page=10)
    return render_template('products/store.html',
    product_category=product_category,
    categories=categories_query(),
    brands=brands_query(),
    product_category_id=product_category_id)
