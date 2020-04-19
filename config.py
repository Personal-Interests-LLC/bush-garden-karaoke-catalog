import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# TODO: gotta clean this up buddy  
# Create connexion app instance, get underlying flask app instance
basedir = os.path.abspath(os.path.dirname(__file__))
connex_app = connexion.App(__name__, specification_dir=basedir)
app = connex_app.app
# Configure the SQLAlchemy, sqlite
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' \
        + os.path.join(basedir, 'kcatalog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create SQLAchemy db instance, init Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# swagger.yml file with API and endpoints defined
connex_app.add_api("swagger.yml")


class Config(object):
    SECRET_KEY = 'placeholder-for-my-future-key-ya-dummy'
    CSRF_ENABLED = True
    TESTING = False
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
