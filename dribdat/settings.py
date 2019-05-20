# -*- coding: utf-8 -*-
"""Application configuration."""
import os

os_env = os.environ

class Config(object):
    """Base configuration."""

    SECRET_KEY = os_env.get('DRIBDAT_SECRET', 'A-big-scary-Secret-goes-HERE.')
    DRIBDAT_APIKEY = os_env.get('DRIBDAT_APIKEY', None)
    DRIBDAT_SLACK_ID = os_env.get('DRIBDAT_SLACK_ID', None)
    DRIBDAT_SLACK_SECRET = os_env.get('DRIBDAT_SLACK_SECRET', None)
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'null'
    CACHE_NO_NULL_WARNING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_NAME = os_env.get('SERVER_URL', '127.0.0.1:5000')
    TIME_ZONE = 'Europe/Zurich'

class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    CACHE_TYPE = os_env.get('DRIBDAT_CACHE_TYPE', 'simple')
    CACHE_MEMCACHED_SERVERS = os_env.get('MEMCACHED_SERVERS', '')
    CACHE_MEMCACHED_USERNAME = os_env.get('MEMCACHED_USERNAME', '')
    CACHE_MEMCACHED_PASSWORD = os_env.get('MEMCACHED_PASSWORD', '')
    SQLALCHEMY_DATABASE_URI = os_env.get('DATABASE_URL', 'postgresql://localhost/example')
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    WTF_CSRF_ENABLED = False  # Allows form testing


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SERVER_NAME = 'localhost'
    WTF_CSRF_ENABLED = False  # Allows form testing
    PRESERVE_CONTEXT_ON_EXCEPTION = False
