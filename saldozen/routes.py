from saldozen import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from saldozen.models import User, ExpenseType, Expense
from saldozen.forms import RegisterForm, LoginForm, EditProfileForm
from saldozen import db
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime


@app.route("/")

@app.route("/home")
@login_required 
def home_page():

    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()

        ## pegar o total
    total_expenses = sum(expense.amount for expense in expenses)

        ## pegar a mais recente
    most_recent_expense = expenses[0] if expenses else 0

    budget = current_user.budget
        # Calcular a porcentagem do orçamento utilizado
    percentage_used = (total_expenses / budget * 100) if budget > 0 else 0

    largest_expense = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.amount.desc()).first()

    return render_template("home.html", total_expenses=total_expenses, 
                            most_recent_expense=most_recent_expense, 
                            largest_expense=largest_expense, datetime=datetime, percentage_used=percentage_used)
   


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
@login_required 
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

@app.route('/lancamentos', methods=['GET', 'POST'])
@login_required 
def expense_page():
    if request.method == 'POST':
        # Adicionar uma nova despesa
        expense_type_id = request.form.get('expense_type_id')
        amount = request.form.get('amount')
        description = request.form.get('description')

        # Criar a nova despesa
        new_expense = Expense(
            user_id=current_user.id,  # Certifique-se de que o usuário está autenticado
            expense_type_id=expense_type_id,
            amount=int(amount),
            description=description,
            date=datetime.now()
        )
        db.session.add(new_expense)

        ## deduzir do user
        current_user.budget -= float(amount)
        
        db.session.commit()
        flash('Despesa adicionada com sucesso!', 'success')
        return redirect(url_for('expense_page'))

    expense_types = ExpenseType.query.all()
    expenses = Expense.query.filter_by(user_id=current_user.id).all()  # Obter as despesas do usuário atual
    return render_template("expense.html", expense_types=expense_types, expenses=expenses)