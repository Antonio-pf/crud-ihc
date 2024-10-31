from saldozen import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from saldozen.models import User
from saldozen.forms import RegisterForm, LoginForm, EditProfileForm
from saldozen import db
from flask_login import login_user, logout_user, current_user


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
        flash("Você foi desconectado!", category="success")

        login_user(user_to_create)

        return redirect(url_for("home_page"))
    if form.errors != {}:  # if there are not errors frmo de validations
        for err_msg in form.errors.values():
            flash(
                f"Ocorreu um erro ao criar usuário: {err_msg}", category="danger")

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
                f"Successo! Você está logado como: {attempted_user.username}",
                category="success",
            )
            return redirect(url_for("home_page"))
        else:
            flash(
               "Nome de usuário e senha não coincidem! Tente novamente", category="danger"
            )

    return render_template("login.html", form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("Você foi desconectado!", category="success")
    return redirect(url_for("login_page"))

@app.route("/sobre")
def about_page():
    return render_template("about.html")

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile_page():
    form = EditProfileForm(current_user=current_user)

    if form.validate_on_submit():
        current_user.username = form.username.data
        
        if form.password1.data:
            current_user.password = form.password1.data
            
        db.session.commit()
        flash('Perfil atualizado com sucesso!', category='success')
        return redirect(url_for('home_page'))  

    # Se o formulário não é válido, mostra os erros
    if form.errors:
        for err_msg in form.errors.values():
            flash(
                f"Ocorreu um erro ao atualizar o perfil: {err_msg}", category="danger"
            )

    form.username.data = current_user.username

    return render_template('profile.html', form=form)
