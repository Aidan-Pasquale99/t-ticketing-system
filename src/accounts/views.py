from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from src import bcrypt, db

from src.accounts.models import User

from .forms import LoginForm, RegisterForm

accounts_bp = Blueprint("accounts", __name__)


# User registration page
# Allows for the creation of new system non-admin users
# Data validation is done here to ensure valid credentials have been passed
@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("core.home"))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Registration successful, you are now logged in.", "success")

        return redirect(url_for("core.home"))

    return render_template("accounts/register.html", form=form)


# Login page
# Data validation is done here to ensure valid credentials have been passed
# Use of SQLAlchemy data objects ensures SQL injection attacks will fail
# UI alerts are used to indicate successful logins and failed attempts
@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("core.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("core.home"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("accounts/login.html", form=form)
    return render_template("accounts/login.html", form=form)


# Logout route
# Executes the logout function, gives the user a visual confirmation, and returns
# to the login page
# This can only be performed by authenticated users due to the @login_required 
# decorator
@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "success")
    return redirect(url_for("accounts.login"))