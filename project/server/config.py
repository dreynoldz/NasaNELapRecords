# project/server/config.py

import os
from contextlib import suppress
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = 'my_precious'
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(
        os.path.join(basedir, 'dev.db'))
    DEBUG_TB_ENABLED = True
    FLASK_DEBUG = 1


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    DEBUG_TB_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'
    DEBUG_TB_ENABLED = False

class SiteSetting():
    """Setup the website defaults."""
    TITLE = 'NasaNE Lap Records'
    DESCRIPTION = 'NasaNE Lap Database'
    HOME = 'Lap Records'
    AUTHOR = 'Aaron Van Blarcom'
    EMAIL = 'aaron@van-blar.com'
    COPYRIGHT = 'AVB Designs'
    TIMEDELTA = 30
