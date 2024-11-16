from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import datetime
from .utils import format_currency 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./saldozen.db"
app.config["SECRET_KEY"] = "6ef60114fb50a5455a267c78"
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)

login_manager.login_view = "login_page"

# Personalize a mensagem e a categoria de erro
login_manager.login_message = "Você precisa fazer login para acessar a conta!"
login_manager.login_message_category = "danger"

@app.template_filter('currency')
def currency_filter(amount):
    return format_currency(amount)

@app.template_filter()
def days_ago(date):
    return (datetime.now() - date).days if date else 0

@app.template_filter('prettier_amount')
def prettier_amount(amount):
    if len(str(amount)) >= 4:
        return f"${str(amount)[:-3]},{str(amount)[-3:]}"
    else:
        return f"${amount}"
    

from .routes import routes
# Importar modelos após a criação do db
from saldozen.models import ExpenseType 
