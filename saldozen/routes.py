from saldozen import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')
