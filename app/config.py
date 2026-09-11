import os

# get the absolute path of the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))

# the base config class holding settings shared by all environments
class Config:
    SECRET_KEY = '82784b5a63535b34'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'instance', 'recipes.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SPOONACULAR_API_KEY = 'ae37dbd5841b48fcb0d3908e250cbdbd'
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'profile_pics')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}