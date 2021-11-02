from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy

class AnonymousUser(AnonymousUserMixin):
    id = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "6194a1bcb55a1b47cee6960ccaaf49"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.anonymous_user = AnonymousUser

from shareFile import routes
