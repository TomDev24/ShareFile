from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    from shareFile.routes.home import home_route
    from shareFile.routes.user import user_route
    app.register_blueprint(home_route)
    app.register_blueprint(user_route)
    return app
