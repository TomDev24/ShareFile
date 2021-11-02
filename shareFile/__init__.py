from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "6194a1bcb55a1b47cee6960ccaaf49"

from shareFile import routes
