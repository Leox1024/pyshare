from flask import request, session, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user
from src.accounts.models import Account

def login_controller():
    username = request.form['username']
    password = request.form['password']

    account = Account.query.filter_by(username=username).first()

    if account and check_password_hash(account.hashed_password, password):
        session['loggedin'] = True
        session['id'] = account.id
        session['username'] = account.username

        login_user(account)
        flash("Logged in successfully!", "success")
        return redirect(url_for('home'))  # Reindirizza alla dashboard
    else:
        
        flash("Incorrect username/password!", "danger")
        return redirect(url_for('accounts.login'))