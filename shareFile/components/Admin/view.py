from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from shareFile.components.User.auth import is_admin
from flask import redirect, url_for, request, session


class MyIndexView(AdminIndexView):
    def is_accessible(self):
        return is_admin(session.get("id"))
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user_route.login', next=request.url))

class CustomAdminView(ModelView):
    def is_accessible(self):
        return is_admin(session.get("id"))
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user_route.login', next=request.url))
