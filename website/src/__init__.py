# Flask
from flask import Flask, session
from flask.helpers import get_root_path
# Dash
import dash
# Models - Must actually import all of them in order to 'db.create_all()' create all of the tables
from .customers.models import Register
from .admin.models import AdminUser
from .supplier.models import Supplier
from .products.models import AddProduct
# App Configuration
from .config import AppConfiguration




def create_app():

    from .extensions import db

    server = Flask(__name__)
    server.config.from_object(AppConfiguration)
    
    register_dashapp(server)
    register_extensions(server)
    register_blueprints(server)    

    return server

def register_dashapp(app):
    from .plotlydash.callbacks import init_callbacks
    from .plotlydash.layout import layout

    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dash_app = dash.Dash(__name__,
                        server=app,
                        url_base_pathname='/dashapp/',
                        assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                        meta_tags=[meta_viewport])

    with app.app_context():
        dash_app.title = 'DashApp'
        dash_app.layout = layout
        init_callbacks(dash_app)

def register_extensions(server):

    from .extensions import db, login, migrate, search

    db.init_app(server)
    login.init_app(server)
    login.login_view = 'customer_route.customer_login'
    migrate.init_app(server, db)
    search.init_app(server)

    with server.app_context():
        db.create_all()

    @login.user_loader
    def load_user(user_id):
        #print('SESSION',session)
        if 'permission' not in session:
            pass
        else:
            if session['permission'] == 'admin':
                print('ADMIN')
                return AdminUser.query.get(int(user_id))
            elif session['permission'] == 'supplier':
                return Supplier.query.get(int(user_id))
            elif session['permission'] == 'customer':
                return Register.query.get(int(user_id))
            else:
                return None

def register_blueprints(server):
    from .customers.routes import customer_route
    from.supplier.routes import s_route
    from .admin.routes import admin_route
    from .products.routes import products
    from .carts.routes import carts

    server.register_blueprint(customer_route, url_prefix='/')
    server.register_blueprint(s_route, url_prefix='/s_rt')
    server.register_blueprint(admin_route, url_prefix='/admin_route')
    server.register_blueprint(products, url_prefix='/products/')
    server.register_blueprint(carts, url_prefix='/carts/')

