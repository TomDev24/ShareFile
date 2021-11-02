from flask import url_for, redirect, render_template, flash
from shareFile.forms import RegForm, LoginForm
from shareFile import app, db, bcrypt
from shareFile.models import User, FileEntry

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Account created for {form.username.data} !")
        return redirect(url_for("home"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #login_user(user)
            flash(f"Welcome back {user.username}!")
            return redirect(url_for("home"))
        else:
            flash("No such account")
    return render_template("login.html", form=form)
