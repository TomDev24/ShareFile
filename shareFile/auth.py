from flask import session
from shareFile.models import User

#accepts user object
def login_user(user):
    session["id"] = user.id
    session["is_authenticated"] = True

def logout_user(user):
    if session["id"]:
        session["is_authenticated"]= False
        session["id"] = None

def cur_user(id):
    if id:
        return User.query.get(int(id))
    else:
        return None
