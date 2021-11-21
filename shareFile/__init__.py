from flask import Flask
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()
admin = Admin(name="shareFile", template_mode="bootstrap3")

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    from shareFile.components.Admin.view import MyIndexView
    admin.init_app(app, index_view=MyIndexView())
    
    from shareFile.routes.home import home_route
    from shareFile.routes.user import user_route
    app.register_blueprint(home_route)
    app.register_blueprint(user_route)
    return app
