import os


class BaseConfig(object):
    DEBUG = True
    FLASK_ADMIN_SWATCH = 'cosmo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "123456"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    WTF_CSRF_ENABLED = True
    OPENAPI_URL_PREFIX = '/api/docs'
    OPENAPI_SWAGGER_UI_PATH = '/'
    OPENAPI_SWAGGER_UI_VERSION = '3.22.0'


class DevConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class TestingConfig(BaseConfig):
    TESTING = True
