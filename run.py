from shareFile import create_app, db, bcrypt, admin
from shareFile.components.User.model import User
from shareFile.components.FileEntry.model import FileEntry, SharedFiles
from shareFile.components.Admin.view import CustomAdminView
from config import Config

app = create_app(Config)
admin.add_view(CustomAdminView(User, db.session))
admin.add_view(CustomAdminView(FileEntry, db.session))
admin.add_view(CustomAdminView(SharedFiles, db.session))

@app.cli.command("initdb")
def initdb():
    db.drop_all()
    db.create_all()
    admin_user = User(username="admin", email="admin@admin.ru", password=bcrypt.generate_password_hash("admin").decode("utf-8"))
    db.session.add(admin_user)
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
