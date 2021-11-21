from flask import session
from shareFile.components.User.model import User

def login_user(user):
    session["id"] = user.id
    session["is_authenticated"] = True

def logout_user(user):
    if session["id"]:
        session["is_authenticated"]= False
        session["id"] = None

def cur_user(id):
    try:
        return User.query.get(int(id))
    except:
        return None

def is_admin(id):
    user = cur_user(id)
    if not user:
        return False
    return user.username == "admin"
