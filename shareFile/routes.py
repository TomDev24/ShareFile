from flask import url_for, redirect, render_template, flash
from shareFile.forms import RegForm, LoginForm, UploadFileForm
from shareFile import app, db, bcrypt
from shareFile.models import User, FileEntry
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Welcome back {user.username}!")
            return redirect(url_for("home"))
        else:
            flash("No such account")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_file(form_file):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_file.filename)
    new_filename = random_hex + f_ext
    new_file_path = os.path.join(app.root_path, 'static/', 'FileCollection/', new_filename)
    form_file.save(new_file_path)
    relative_path = url_for('static', filename='FileCollection/' + new_filename)
    return relative_path, new_filename

@app.route("/account", methods = ["GET", "POST"])
@login_required
def account():
    form = UploadFileForm()
    files = FileEntry.query.filter_by(user_id=current_user.id).all()
    if form.validate_on_submit():
        _, new_filename = save_file(form.file.data)
        new_file = FileEntry(file_path=new_filename, access=form.access_setting.data, download_amount=0,
                            filename=form.filename.data, user_id=current_user.id)
        db.session.add(new_file)
        db.session.commit()
        flash("File uploaded")
        return redirect(url_for("account"))
    return render_template("account.html", files=files, form=form)
