from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from shareFile.config import Config

#before here was app variable which is imported in different files
#there is solution - replace app from module to -> curent_app from flask
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    #its better to have bluepritns here
    from shareFile.routes import main
    app.register_blueprint(main)
    return app
