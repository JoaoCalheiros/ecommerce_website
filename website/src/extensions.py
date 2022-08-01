from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_msearch import Search

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
search = Search()
