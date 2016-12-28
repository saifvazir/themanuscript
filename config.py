import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'the quick brown fox jumps over the lazy dog'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
   # SQLALCHEMY_DATABASE_URI = "postgresql://ankitesh:postgres@localhost/test"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ankitesh:tiger@localhost/tmsprod'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ankitesh:tiger@localhost/tmsdev'


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ankitesh:tiger@localhost/test'

