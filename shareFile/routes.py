from flask import url_for, redirect, render_template, flash
from shareFile.forms import RegForm, LoginForm
from shareFile import app

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data} !")
        return redirect(url_for("home"))
    return render_template("register.html", form=form)

@app.route("/login")
def login():
    return "login"
