import os


# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = "\x0c\x1d\x18\xde<J\x046!(\x8c\xe6\x9ae\xb2\xfc5\x8d\x87\xfe\x8f\xb4-\xfa"
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


