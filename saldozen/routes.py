from saldozen import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from saldozen.models import User, ExpenseType, Expense, Income
from saldozen.forms import RegisterForm, LoginForm, EditProfileForm, IncomeForm, ExpenseForm
from saldozen import db
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
import requests
from decimal import Decimal
import json
import io
import zipfile
from flask import send_file

@app.route("/")
@app.route("/home")
@login_required 
def home_page():
    # Carregar as despesas do usuário atual
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()

    # Calcular o total de despesas
    total_expenses = sum(expense.amount for expense in expenses)
    print(type(total_expenses))  

    # Pegar a despesa mais recente
    most_recent_expense = expenses[0] if expenses else None

    # Pegar o orçamento do usuário
    budget = current_user.budget
    print(type(budget))  

    percentage_used = (total_expenses / budget * 100) if budget > 0 else 0
    largest_expense = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.amount.desc()).first()

    expense_types = ExpenseType.query.all()
    formIncome = IncomeForm()
    formExpense = ExpenseForm()
    if formIncome.validate_on_submit():
        new_income = Income(
            user_id=current_user.id,
            amount=Decimal(formIncome.amount.data),  
            description=formIncome.description.data,
            date=formIncome.date.data or datetime.now()
        )
        db.session.add(new_income)

        current_user.budget += new_income.amount
        db.session.commit()

        flash('Entrada de receita adicionada com sucesso!', 'success')
        return redirect(url_for('home_page'))  
   
    if formExpense.validate_on_submit():
        new_expense = Expense(
            user_id=current_user.id,
            amount=Decimal(formExpense.amount.data),  
            description=formExpense.description.data,
            date=formExpense.date.data or datetime.now()
        )
        db.session.add(new_expense)
        db.session.commit()

        flash('Entrada de despesa adicionada com sucesso!', 'success')
        return redirect(url_for('home_page'))

    return render_template("home.html", 
                           total_expenses=total_expenses, 
                           most_recent_expense=most_recent_expense, 
                           largest_expense=largest_expense, 
                           datetime=datetime, 
                           percentage_used=percentage_used, 
                           formIncome=formIncome, 
                           formExpense=formExpense,
                           expense_types=expense_types
                           )


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
        flash("Bem-vindo...seja zen!", category="success")

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
               "Nome de usuário e senha não coincidem! Tente novamente", category="danger")
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

    # Se o formulário não é válido, mostro os erros
    if form.errors:
        for err_msg in form.errors.values():
            flash(
                f"Ocorreu um erro ao atualizar o perfil: {err_msg}", category="danger")

    form.username.data = current_user.username
    return render_template('profile.html', form=form)

@app.route('/despesas', methods=['GET', 'POST'])
@login_required 
def expense_page():
    if request.method == 'POST':
        # Adicionar uma nova despesa
        expense_type_id = request.form.get('expense_type_id')
        amount = request.form.get('amount')
        description = request.form.get('description')

        new_expense = Expense(
            user_id=current_user.id,  
            expense_type_id=expense_type_id,
            amount=int(amount),
            description=description,
            date=datetime.now()
        )
        db.session.add(new_expense)

        ## a cada entrada de despesa é debitado do saldo total
        current_user.budget -= Decimal(amount)
        
        db.session.commit()
        flash('Despesa adicionada com sucesso!', 'success')
        return redirect(url_for('expense_page'))

    expense_types = ExpenseType.query.all()
    expenses = Expense.query.filter_by(user_id=current_user.id).all()  # Obter as despesas do usuário atual
    return render_template("expense.html", expense_types=expense_types, expenses=expenses)

@app.route('/export-data')
@login_required
def export_expense():
   
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    print('pasou')
    print(expenses)
    if len(expenses) == 0: 
        flash('Não há despesas para exportar!', 'info')
        return redirect(url_for('home_page'))

    expenses_data = [
        {
            "id": expense.id,
            "user_id": expense.user_id,
            "expense_type_id": expense.expense_type_id,
            "amount": expense.amount,
            "description": expense.description,
            "date": expense.date.isoformat() 
        }
        for expense in expenses
    ]
    json_data = json.dumps(expenses_data, ensure_ascii=False, indent=4)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("expenses.json", json_data)  

    zip_buffer.seek(0)  

    return send_file(zip_buffer, as_attachment=True, download_name="expenses.zip", mimetype="application/zip")


@app.route('/add_income', methods=['GET', 'POST'])
@login_required
def add_income():
    formIncome = IncomeForm()
    if formIncome.validate_on_submit():
 
        new_income = Income(
            user_id=current_user.id,
            amount=formIncome.amount.data,
            description=formIncome.description.data,
            date=formIncome.date.data
        )
        db.session.add(new_income)

        # Atualizar o budget do usuário
        current_user.budget += formIncome.amount.data  # Adiciona a nova entrada ao budget

        db.session.commit()
        flash('Entrada adicionada com sucesso!', 'success')
        return redirect(url_for('home_page'))

    return render_template('add_income.html', formIncome=formIncome)

@app.route('/add-expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    formExpense = ExpenseForm()

    formExpense.expense_type_id.choices = [(et.id, et.name) for et in ExpenseType.query.all()]

    if formExpense.validate_on_submit():
        input_date = formExpense.date.data

        new_expense = Expense(
            user_id=current_user.id, 
            expense_type_id=formExpense.expense_type_id.data,  
            amount=formExpense.amount.data,  
            date=datetime.combine(input_date, datetime.now().time()), 
            description=formExpense.description.data 
        )
        
        db.session.add(new_expense)
        
        current_user.budget -= new_expense.amount 
        db.session.commit()  

        flash('Despesa adicionada com sucesso!', 'success') 
        return redirect(url_for('home_page'))  
    else:
        print(formExpense.errors) 

    return render_template("home_page.html", formExpense=formExpense)   


@app.route('/delete-expense/<int:id_expense>', methods=['GET'])
@login_required
def delete_expense(id_expense):
    expense = Expense.query.get(id_expense)
    user = current_user
    if expense:
        user.budget += expense.amount
        db.session.delete(expense)
        db.session.commit()
        flash("Despesa excluída com sucesso.", "success")
    else:
        flash("Despesa não encontrada.", "error")
    return redirect(url_for('expense_page')) 