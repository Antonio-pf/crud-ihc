from saldozen import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from saldozen.models import User
from saldozen.forms import RegisterForm, LoginForm
from saldozen import db
from flask_login import login_user, logout_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password1.data,
        )
        db.session.add(user_to_create)
        db.session.commit()
        flash("You have been logged out!", category="success")

        login_user(user_to_create)

        return redirect(url_for("home_page"))
    if form.errors != {}:  # if there are not errors frmo de validations
        for err_msg in form.errors.values():
            flash(
                f"There was an error with creating a user: {err_msg}", category="danger"
            )

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()

        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(
                f"Success! You are logged is as: {attempted_user.username}",
                category="success",
            )
            return redirect(url_for("home_page"))
        else:
            flash(
                "Username and password not match! Please try again", category="danger"
            )

    return render_template("login.html", form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out!", category="success")
    return redirect(url_for("login_page"))

@app.route("/sobre")
def about_page():
    return render_template("about.html")