import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "6194a1bcb55a1b47cee6960ccaaf49"
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or 'sqlite:///site.db'
    FLASK_ADMIN_SWATCH = 'cyborg'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
