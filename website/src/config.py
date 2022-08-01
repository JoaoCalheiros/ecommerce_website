import os
from password_strength import PasswordPolicy
from password_strength import PasswordStats


class AppConfiguration:
    DEBUG = True
    DB_NAME = 'test.db'

    SECRET_KEY = os.urandom(10)

    SQLALCHEMY_DATABASE_URI = f'sqlite:///database/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # EXPLAIN_TEMPLATE_LOADING = True

    # https://pythonhosted.org/Flask-Uploads/
    basedir = os.path.abspath(os.path.dirname(__file__))
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'static')




# Password restrictions
policy = PasswordPolicy.from_names(
    strength=0.2
)

def check_pass_strength(password):
    pass_cred = PasswordStats(password)
    check_policy = policy.test(password)

    # Return True if password does not meet the requirements
    # Setting a low value for testing purposes
    if pass_cred.strength() < 0.2:
        return True
    else:
        return False
