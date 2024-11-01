from saldozen import db, login_manager
from saldozen import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f"${str(self.budget)[:-3]},{str(self.budget)[-3:]} "
        else:
            return f"${self.budget}"

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
    amount = db.Column(db.Integer(), nullable=False)  # Valor da despesa
    date = db.Column(db.DateTime(), nullable=False)  # Data da despesa
    description = db.Column(db.String(length=200), nullable=True)  # Descrição da despesa

    # Relacionamento com User
    user = db.relationship('User', backref='expenses', lazy=True)

    @property
    def prettier_amount(self):
        if len(str(self.amount)) >= 4:
            return f"${str(self.amount)[:-3]},{str(self.amount)[-3:]} "
        else:
            return f"${self.amount}"
    
    def __repr__(self):
        return f'<Expense {self.amount} on {self.date}>'
