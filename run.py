import click
from shareFile import create_app, db, bcrypt
from shareFile.components.User.model import User
from config import Config

app = create_app(Config)

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
