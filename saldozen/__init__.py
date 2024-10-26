from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./saldozen.db'
app.config['SECRET_KEY'] = '6ef60114fb50a5455a267c78'
db = SQLAlchemy(app)

from saldozen import routes