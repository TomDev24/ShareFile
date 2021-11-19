import click
from shareFile import create_app, db, bcrypt
from shareFile.components.User.model import User
from shareFile.components.User.auth import is_admin
from shareFile.components.FileEntry.model import FileEntry, SharedFiles
from config import Config
from flask_admin import Admin
from flask import redirect, url_for, request, session
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

app = create_app(Config)
app.config['FLASK_ADMIN_SWATCH'] = 'cyborg'

class MyIndexView(AdminIndexView):
    def is_accessible(self):
        return is_admin(session.get("id"))
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user_route.login', next=request.url))

admin = Admin(app, name="shareFile", template_mode="bootstrap3", index_view=MyIndexView())

class CustomAdminView(ModelView):
    def is_accessible(self):
        return is_admin(session.get("id"))
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user_route.login', next=request.url))

admin.add_view(CustomAdminView(User, db.session))
admin.add_view(CustomAdminView(FileEntry, db.session))
admin.add_view(CustomAdminView(SharedFiles, db.session))

@app.cli.command("initdb")
#@click.argument("name")
def initdb():
    db.drop_all()
    db.create_all()
    admin_user = User(username="admin", email="admin@admin.ru", password=bcrypt.generate_password_hash("admin").decode("utf-8"))
    db.session.add(admin_user)
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
