import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-prod')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///jegeekutile.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False

    PASSWORD_RESET_SALT = os.getenv('PASSWORD_RESET_SALT', 'reset-salt-change-in-prod')
    PASSWORD_RESET_EXPIRY_HOURS = 1

    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    SMTP_FROM_EMAIL = os.getenv('SMTP_FROM_EMAIL', 'noreply@jegeekutile.local')

    BOOTSTRAP_TEST_USERS = os.getenv('BOOTSTRAP_TEST_USERS', 'false').lower() == 'true'
    CSRF_ENABLED = True
    RATE_LIMIT_ENABLED = True
    LOGIN_RATE_LIMIT_MAX = int(os.getenv('LOGIN_RATE_LIMIT_MAX', 10))
    LOGIN_RATE_LIMIT_WINDOW = int(os.getenv('LOGIN_RATE_LIMIT_WINDOW', 60))
    RESET_RATE_LIMIT_MAX = int(os.getenv('RESET_RATE_LIMIT_MAX', 5))
    RESET_RATE_LIMIT_WINDOW = int(os.getenv('RESET_RATE_LIMIT_WINDOW', 300))

    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_NAME = 'jegeekutile_session'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SESSION_COOKIE_SECURE = False
    RATE_LIMIT_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
