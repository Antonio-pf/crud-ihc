from saldozen import db, login_manager
from saldozen import bcrypt
from flask_login import UserMixin
from sqlalchemy import Numeric

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    budget = db.Column(Numeric(10, 2), nullable=False, default=1000)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def prettier_budget(self):
        formatted_budget = f"{self.budget:.2f}"
        whole, decimal = formatted_budget.split('.')
        formatted_whole = f"{int(whole):,}".replace(',', '.')
        return f"${formatted_whole},{decimal}"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode(
            "utf-8"
        )

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def add_expense(self, expense_type_id, amount, date=None, description=None):
        from datetime import datetime
        if date is None:
            date = datetime.now()  

        new_expense = Expense(user_id=self.id, expense_type_id=expense_type_id,
                              amount=amount, date=date, description=description)
        db.session.add(new_expense)
        db.session.commit()

    
class ExpenseType(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)

    # Define o relacionamento
    expenses = db.relationship('Expense', backref='expense_type', lazy=True)

    def __repr__(self):
        return f'<ExpenseType {self.name}>'
    
class Expense(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    expense_type_id = db.Column(db.Integer(), db.ForeignKey('expense_type.id'), nullable=False)
    amount = db.Column(Numeric(10, 2), nullable=False)  
    date = db.Column(db.DateTime(), nullable=False)  
    description = db.Column(db.String(length=200), nullable=True)  

    # Relacionamento com User
    user = db.relationship('User', backref='expenses', lazy=True)

    @property
    def prettier_amount(self):
        formatted_amount = f"{self.amount:.2f}"
        whole, decimal = formatted_amount.split('.')
        formatted_whole = f"{int(whole):,}".replace(',', '.')
        return f"${formatted_whole},{decimal}"

    
    def __repr__(self):
        return f'<Expense {self.amount} on {self.date}>'


class Income(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(Numeric(10, 2), nullable=False) 
    description = db.Column(db.String(length=200), nullable=True)
    date = db.Column(db.DateTime(), nullable=False)

    user = db.relationship('User', backref='incomes', lazy=True)

    def __repr__(self):
        return f'<Income {self.amount} on {self.date}>'
