from saldozen import db, login_manager
from saldozen import bcrypt
from flask_login import UserMixin
from sqlalchemy import Numeric, func, label
from datetime import datetime, timedelta
from decimal import Decimal

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    budget = db.Column(Numeric(10, 2), nullable=False, default=0)
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
    
    @staticmethod
    def get_expenses_last_month(user_id):
        now = datetime.now()
        first_day_of_last_month = datetime(now.year, now.month - 1, 1) if now.month > 1 else datetime(now.year - 1, 12, 1)
        last_day_of_last_month = datetime(now.year, now.month, 1) - timedelta(days=1)
        
        # retorno as despesas do mes passado
        return Expense.query.filter(
            Expense.user_id == user_id,
            Expense.date >= first_day_of_last_month,
            Expense.date <= last_day_of_last_month
        ).order_by(Expense.date.desc()).all()

    @staticmethod
    def get_expenses_last_month_sum(user_id):
        # Obtendo a coleção de despesas do mês passado
        expenses = Expense.get_expenses_last_month(user_id)
        
        # Calculando a soma dos valores diretamente da coleção
        total_sum = sum(expense.amount for expense in expenses)

        return total_sum
    @staticmethod
    def get_expenses_percentage(user_id, total_income):
        if total_income == 0:
            raise ValueError("O total de receitas não pode ser zero.")
        total_income_decimal = Decimal(total_income)


        top_expenses = (
            db.session.query(
                Expense.expense_type_id,
                ExpenseType.name,  # Incluindo o nome do tipo de despesa
                label('total', func.sum(Expense.amount))
            )
            .join(ExpenseType, Expense.expense_type_id == ExpenseType.id)  # Realizando o join
            .filter(Expense.user_id == user_id)
            .group_by(Expense.expense_type_id, ExpenseType.name)  # Agrupando pelo nome do tipo
            .order_by(func.sum(Expense.amount).desc())
            .limit(3)
            .all()
        )

        top_ids = [expense.expense_type_id for expense in top_expenses]

        other_expenses = (
            db.session.query(
                label('total', func.sum(Expense.amount))
            )
            .filter(
                Expense.user_id == user_id,
                ~Expense.expense_type_id.in_(top_ids)
            )
            .scalar() or 0
        )

        results = [
            {
                "type": expense.name,
                "total": expense.total,
                "percentage": round((expense.total / total_income_decimal) * 100, 2),
            }
            for expense in top_expenses
        ]

        results.append({
            "type": "Outros",
            "total": other_expenses,
            "percentage": round((other_expenses / total_income_decimal) * 100, 2),
        })

        return results
    
    def __repr__(self):
        return f'<Expense {self.amount} on {self.date}>'


class Income(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(Numeric(10, 2), nullable=False) 
    description = db.Column(db.String(length=200), nullable=True)
    date = db.Column(db.DateTime(), nullable=False)

    user = db.relationship('User', backref='incomes', lazy=True)


    @staticmethod
    def get_total_income(user_id):
        total_income = (
            db.session.query(func.sum(Income.amount))
            .filter(Income.user_id == user_id)
            .scalar() or 0
        )
        return float(total_income)

    def __repr__(self):
        return f'<Income {self.amount} on {self.date}>'
