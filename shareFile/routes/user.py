from flask import url_for, redirect, render_template, flash, session
from flask import Blueprint
from shareFile import bcrypt
from shareFile.components.FileEntry.forms import UploadFileForm
from shareFile.components.User.forms import RegForm, LoginForm
from shareFile.components.FileEntry.model import FileEntry
from shareFile.components.User.model import User
from shareFile.components.User.auth import login_user, logout_user, cur_user

user_route = Blueprint("user_route", __name__)

@user_route.route("/register", methods=["GET"])
def register():
    if cur_user(session.get("id")):
        return redirect(url_for('home_route.home'))
    form = RegForm()
    return render_template("register.html", form=form)

@user_route.route("/register", methods=["POST"])
def register_post():
    form = RegForm()
    if form.validate_on_submit():
        User.create_user(form)
        flash(f"Account created for {form.username.data} !")
        return redirect(url_for("home_route.home"))
    return render_template("register.html", form=form)

@user_route.route("/login", methods=["GET"])
def login():
    if cur_user(session.get("id")): #current_user.is_authenticated:
        return redirect(url_for('home_route.home'))
    form = LoginForm()
    return render_template("login.html", form=form)

@user_route.route("/login", methods=["POST"])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.by_user_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Welcome back {user.username}!")
            return redirect(url_for("home_route.home"))
    flash("No such account")
    return render_template("login.html", form=form)

@user_route.route("/logout")
def logout():
    current_user = cur_user(session.get("id"))
    if current_user:
        logout_user( current_user )
    return redirect(url_for('home_route.home'))

@user_route.route("/account", methods = ["GET"])
def account():
    current_user = cur_user(session.get("id"))
    if not current_user:
        return redirect(url_for("user_route.register"))
    form = UploadFileForm()
    files = FileEntry.get_user_files(current_user)
    return render_template("account.html", files=files, form=form, current_user=current_user)

@user_route.route("/account", methods = ["POST"])
def account_post():
    form = UploadFileForm()
    current_user = cur_user(session.get("id"))
    files = FileEntry.get_user_files(current_user)
    if form.validate_on_submit():
        FileEntry.upload_file(form, current_user)
        flash("File uploaded")
        return redirect(url_for("user_route.account"))
    return render_template("account.html", files=files, form=form, current_user=current_user)
